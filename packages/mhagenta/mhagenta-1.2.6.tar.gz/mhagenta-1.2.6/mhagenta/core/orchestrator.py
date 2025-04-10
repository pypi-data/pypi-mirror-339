import asyncio
import logging
import os
import shutil
import sys
import time
from asyncio import TaskGroup
from dataclasses import dataclass
from io import TextIOWrapper
from os import PathLike
import socket
from pathlib import Path
from typing import Any, Iterable, Literal, Self
import subprocess
import signal

import dill
import docker
import pika
from pika.adapters import BlockingConnection
from pika.channel import Channel
from pika.exceptions import AMQPConnectionError
from docker.errors import NotFound
from docker.models.containers import Container
from docker.models.images import Image

import mhagenta
from mhagenta.bases import *
from mhagenta.containers import *
from mhagenta.core.connection import Connector, RabbitMQConnector
from mhagenta.utils import DEFAULT_PORT, DEFAULT_RMQ_IMAGE
from mhagenta.utils.common import DEFAULT_LOG_FORMAT, Directory
from mhagenta.environment import MHAEnvBase
# from mhagenta.utils.common.classes import EDirectory
from mhagenta.gui import Monitor
from mhagenta.utils.common.classes import EDirectory


@dataclass
class AgentEntry:
    agent_id: str
    kwargs: dict[str, Any]
    dir: Path | None = None
    save_dir: Path | None = None
    image: Image | None = None
    container: Container | None = None
    port_mapping: dict[int, int] | None = None
    num_copies: int = 1
    save_logs: bool = True
    tags: Iterable[str] | None = None
    # port: int | None = None

    @property
    def module_ids(self) -> list[str]:
        module_ids = []
        keys = ('perceptors',
                'actuators',
                'll_reasoners',
                'learners',
                'knowledge',
                'hl_reasoners',
                'goal_graphs',
                'memory')
        for key in keys:
            if self.kwargs[key] is None:
                continue
            if isinstance(self.kwargs[key], Iterable):
                for module in self.kwargs[key]:
                    module_ids.append(module.module_id)
            else:
                module_ids.append(self.kwargs[key].module_id)
        return module_ids

@dataclass
class EnvironmentEntry:
    environment: dict[str, Any]
    address: dict[str, Any]
    dir: Path | None = None
    tags: list[str] | None = None
    process: subprocess.Popen | None = None


class Orchestrator:
    """Orchestrator class that handles MHAgentA execution.

    Orchestrator handles definition of agents and their consequent containerization and deployment. It also allows you
    to define default parameters shared by all the agents handles by it (can be overridden by individual agents)

    """
    SAVE_SUBDIR = 'out/save'
    LOG_CHECK_FREQ = 1.

    def __init__(self,
                 save_dir: str | PathLike,
                 port_mapping: dict[int, int] | None = None,
                 step_frequency: float = 1.,
                 status_frequency: float = 5.,
                 control_frequency: float = -1.,
                 exec_start_time: float | None = None,
                 agent_start_delay: float = 60.,
                 exec_duration: float = 60.,
                 save_format: Literal['json', 'dill'] = 'json',
                 resume: bool = False,
                 log_level: int = logging.INFO,
                 log_format: str | None = None,
                 status_msg_format: str = '[status_upd]::{}',
                 module_start_delay: float = 2.,
                 connector_cls: type[Connector] = RabbitMQConnector,
                 connector_kwargs: dict[str, Any] | None = None,
                 mas_rmq_uri: str | Literal['default'] | None = None,
                 mas_rmq_close_on_exit: bool = True,
                 mas_rmq_exchange_name: str | None = None,
                 save_logs: bool = True
                 ) -> None:
        """
        Constructor method for Orchestrator.

        Args:
            save_dir (str | PathLike): Root directory for storing agents' states, logs, and temporary files.
            port_mapping (dict[int, int], optional): Mapping between internal docker container ports and host ports.
            step_frequency (float, optional, default=1.0): For agent modules with periodic step functions, the
                frequency in seconds of the step function calls that modules will try to maintain (unless their
                execution takes longer, then the next iteration will be scheduled without a time delay).
            status_frequency (float, optional, default=10.0): Frequency with which agent modules will report their
                statuses to the agent's root controller (error statuses will be reported immediately, regardless of
                the value).
            control_frequency (float, optional): Frequency of agent modules' internal clock when there's no tasks
                pending. If undefined or not positive, there will be no scheduling delay.
            exec_start_time (float, optional): Unix timestamp in seconds of when the agent's execution will try to
                start (unless agent's initialization takes longer than that; in this case the agent will start
                execution as soon as it finishes initializing). If not specified, agents will start execution
                immediately after their initialization.
            agent_start_delay (float, optional, default=60.0): Delay in seconds before agents starts execution. Use when
                `exec_start_time` is not defined to stage synchronous agents start at `agent_start_delay` seconds from
                the `run()` or `arun()` call.
            exec_duration (float, optional, default=60.0):  Time limit for agent execution in seconds. All agents will
                timeout after this time.
            save_format (Literal['json', 'dill'], optional, default='json'): Format of agent modules state save files. JSON
                is more restrictive of what fields the states can include, but it is readable by humans.
            resume (bool, optional, default=False): Specifies whether to use save module states when restarting an
                agent with preexisting ID.
            log_level (int, optional, default=logging.INFO): Logging level.
            log_format (str, optional): Format of agent log messages. Defaults to
                `[%(agent_time)f|%(mod_time)f|%(exec_time)s][%(levelname)s]::%(tags)s::%(message)s`
            status_msg_format (str, optional): Format of agent status messages for external monitoring. Defaults to
                `[status_upd]::{}`
            connector_cls (type[Connector], optional, default=RabbitMQConnector): internal connector class that
                implements communication between modules. MHAgentA agents use RabbitMQ-based connectors by default.
            connector_kwargs (dict[str, Any], optional): Additional keyword arguments for connector. For
                RabbitMQConnector, the default parameters are: {`host`: 'localhost', `port`: 5672, `prefetch_count`: 1}.
            mas_rmq_uri (str, optional): URI of RabbitMQ server for multi-agent communication. Will try to start
                a RabbitMQ docker server at localhost:5672 if 'default'.
            mas_rmq_close_on_exit (bool, optional, default=True): Whether to close RabbitMQ server when exiting.
            mas_rmq_exchange_name (str, optional): Name of RabbitMQ exchange for inter-agent communication.
                Defaults to 'mhagenta'.
            save_logs (bool, optional, default=True): Whether to save agent logs. If True, saves each agent's logs to
                `<agent_id>.log` at the root of the `save_dir`. Defaults to True.
        """
        if os.name != 'nt' and os.name != 'posix':
            raise RuntimeError(f'OS {os.name} is not supported.')

        self._agents: dict[str, AgentEntry] = dict()
        self._environment: EnvironmentEntry | None = None

        save_dir = Path(save_dir).resolve()
        if isinstance(save_dir, str):
            save_dir = Path(save_dir)
        if not save_dir.exists():
            save_dir.mkdir(parents=True, exist_ok=True)
        self._save_dir = save_dir

        self._package_dir = str(Path(mhagenta.__file__).parent.resolve())

        self._connector_cls = connector_cls if connector_cls else RabbitMQConnector
        if connector_kwargs is None and connector_cls == RabbitMQConnector:
            self._connector_kwargs = {
                'host': 'localhost',
                'port': 5672,
                'prefetch_count': 1
            }
        else:
            self._connector_kwargs = connector_kwargs

        self._port_mapping = port_mapping if port_mapping else {}

        self._step_frequency = step_frequency
        self._status_frequency = status_frequency
        self._control_frequency = control_frequency
        self._module_start_delay = module_start_delay
        self._exec_start_time = exec_start_time
        self._exec_duration_sec = exec_duration
        self._agent_start_delay = agent_start_delay

        self._save_format = save_format
        self._resume = resume

        self._log_level = log_level
        self._log_format = log_format if log_format else DEFAULT_LOG_FORMAT
        self._status_msg_format = status_msg_format

        self._save_logs = save_logs

        self._mas_rmq_uri = mas_rmq_uri if mas_rmq_uri != 'default' else 'localhost:5672'
        self._mas_rmq_uri_internal = mas_rmq_uri if mas_rmq_uri != 'default' else 'localhost:5672'
        if 'localhost' in self._mas_rmq_uri_internal:
            self._mas_rmq_uri_internal = self._mas_rmq_uri_internal.replace('localhost', EDirectory.localhost_linux if sys.platform == 'linux' else EDirectory.localhost_win)
        self._mas_rmq_close_on_exit = mas_rmq_close_on_exit
        self._mas_rmq_container: Container | None = None
        self._mas_rmq_exchange_name = mas_rmq_exchange_name

        self._start_time: float = -1.
        self._simulation_end_ts = -1.

        self._docker_client: docker.DockerClient | None = None
        self._rabbitmq_image: Image | None = None
        self._base_image: Image | None = None

        self._task_group: TaskGroup | None = None
        self._force_run = False

        self._docker_init()

        self._monitor: Monitor | None = None

        self._running = False
        self._stopping = False
        self._all_stopped = False

    def _docker_init(self) -> None:
        self._docker_client = docker.from_env()

    def set_environment(self,
                        base: MHAEnvBase,
                        env_id: str = "environment",
                        host: str | None = 'localhost',
                        port: int | None = 5672,
                        exec_duration: float | None = None,
                        exchange_name: str | None = None,
                        log_tags: list[str] | None = None,
                        log_level: int | str | None = None,
                        log_format: str | None = None,
                        tags: Iterable[str] | None = None
                        ) -> None:
        from mhagenta.defaults.communication.rabbitmq import RMQEnvironment
        if host is None:
            mas_host, mas_port = self._mas_rmq_uri.split(':')
            host = mas_host
            if port is None:
                port = mas_port
        # if host == 'localhost':
        #     if sys.platform == 'linux':
        #         host = EDirectory.localhost_linux
        #     else:
        #         host = EDirectory.localhost_win
        env_dir = self._save_dir.resolve() / env_id
        env_dir.mkdir(parents=True, exist_ok=True)
        environment = {
            'env_class': RMQEnvironment,
            'base': base,
            'env_id': env_id,
            'host': host,
            'port': port,
            'exec_duration': (exec_duration if exec_duration else self._exec_duration_sec) + self._agent_start_delay,
            'exchange_name': exchange_name if exchange_name is not None else self._mas_rmq_exchange_name,
            'start_time_reference': None,
            'save_dir': env_dir,
            'save_format': self._save_format,
            'log_id': env_id,
            'log_tags': log_tags if log_tags is not None else [],
            'log_format': log_format if log_format is not None else self._log_format,
            'log_level': log_level if log_level is not None else self._log_level,
            'tags': tags
        }
        self._environment = EnvironmentEntry(
            environment=environment,
            address={
                'exchange_name': environment['exchange_name'],
                'env_id': env_id
            },
            dir=env_dir,
            tags=tags
        )

    def _update_external_host(self, module: ActuatorBase | PerceptorBase):
        if 'external' in module.tags and module.conn_params['host'] == 'localhost':
            module.conn_params['host'] = EDirectory.localhost_linux if sys.platform == 'linux' else EDirectory.localhost_win

    def add_agent(self,
                  agent_id: str,
                  perceptors: Iterable[PerceptorBase] | PerceptorBase,
                  actuators: Iterable[ActuatorBase] | ActuatorBase,
                  ll_reasoners: Iterable[LLReasonerBase] | LLReasonerBase,
                  learners: Iterable[LearnerBase] | LearnerBase | None = None,
                  knowledge: Iterable[KnowledgeBase] | KnowledgeBase | None = None,
                  hl_reasoners: Iterable[HLReasonerBase] | HLReasonerBase | None = None,
                  goal_graphs: Iterable[GoalGraphBase] | GoalGraphBase | None = None,
                  memory: Iterable[MemoryBase] | MemoryBase | None = None,
                  num_copies: int = 1,
                  step_frequency: float | None = None,
                  status_frequency: float | None = None,
                  control_frequency: float | None = None,
                  exec_start_time: float | None = None,
                  start_delay: float = 0.,
                  exec_duration: float | None = None,
                  resume: bool | None = None,
                  requirements_path: PathLike | None = None,
                  log_level: int | None = None,
                  port_mapping: dict[int, int] | None = None,
                  connector_cls: type[Connector] | None = None,
                  connector_kwargs: dict[str, Any] | None = None,
                  save_logs: bool | None = None,
                  tags: Iterable[str] | None = None
                  ) -> None:
        """Define an agent model to be added to the execution.

        This can be either a single agent, a set of identical agents following the same structure model.

        Args:
            agent_id (str): A unique identifier for the agent.
            perceptors (Iterable[PerceptorBase] | PerceptorBase): Definition(s) of agent's perceptor(s).
            actuators (Iterable[ActuatorBase] | ActuatorBase): Definition(s) of agent's actuator(s).
            ll_reasoners (Iterable[LLReasonerBase] | LLReasonerBase): Definition(s) of agent's ll_reasoner(s).
            learners (Iterable[LearnerBase] | LearnerBase, optional): Definition(s) of agent's learner(s).
            knowledge (Iterable[KnowledgeBase] | KnowledgeBase, optional): Definition(s) of agent's knowledge model(s).
            hl_reasoners (Iterable[HLReasonerBase] | HLReasonerBase, optional): Definition(s) of agent's hl_reasoner(s).
            goal_graphs (Iterable[GoalGraphBase] | GoalGraphBase, optional): Definition(s) of agent's goal_graph(s).
            memory (Iterable[MemoryBase] | MemoryBase, optional): Definition(s) of agent's memory structure(s).
            num_copies (int, optional, default=1): Number of copies of the agent to instantiate at runtime.
            step_frequency (float, optional): For agent modules with periodic step functions, the frequency in seconds
                of the step function calls that modules will try to maintain (unless their execution takes longer, then
                the next iteration will be scheduled without a time delay). Defaults to the Orchestrator's
                `step_frequency`.
            status_frequency (float, optional): Frequency with which agent modules will report their statuses to the
                agent's root controller (error statuses will be reported immediately, regardless of the value).
                Defaults to the Orchestrator's `status_frequency`.
            control_frequency (float, optional): Frequency of agent modules' internal clock when there's no tasks
                pending. If undefined or not positive, there will be no scheduling delay. Defaults to the
                Orchestrator's `control_frequency`.
            exec_start_time (float, optional): Unix timestamp in seconds of when the agent's execution will try to
                start (unless agent's initialization takes longer than that; in this case the agent will start
                execution as soon as it finishes initializing). Defaults to the Orchestrator's `exec_start_time`.
            start_delay (float, optional, default=0.0): A time offset from the global execution time start when this agent will
                attempt to start its own execution.
            exec_duration (float, optional): Time limit for agent execution in seconds. The agent will timeout after
                this time. Defaults to the Orchestrator's `exec_duration`.
            resume (bool, optional): Specifies whether to use save module states when restarting an agent with
                preexisting ID. Defaults to the Orchestrator's `resume`.
            requirements_path (PathLike, optional): Additional agent requirements to install on agent side.
            log_level (int, optional):  Logging level for the agent. Defaults to the Orchestrator's `log_level`.
            port_mapping (dict[int, int], optional): Mapping between internal docker container ports and host ports.
                Defaults to the Orchestrator's `port_mapping`.
            connector_cls (type[Connector], optional): internal connector class that implements communication between
                modules. Defaults to the Orchestrator's `connector_cls`.
            connector_kwargs (dict[str, Any], optional): Additional keyword arguments for connector. Defaults to
                the Orchestrator's `connector_kwargs`.
            save_logs (bool, optional): Whether to save agent logs. If True, saves the agent's logs to
                `<agent_id>.log` at the root of the `save_dir`. Defaults to the orchestrator's `save_logs`.
            tags (Iterable[str], optional): a list of tags associated with this agent for directory search.

        """
        if isinstance(actuators, Iterable):
            for actuator in actuators:
                self._update_external_host(actuator)
        else:
            self._update_external_host(actuators)

        if isinstance(perceptors, Iterable):
            for perceptor in perceptors:
                self._update_external_host(perceptor)
        else:
            self._update_external_host(perceptors)

        kwargs = {
            'agent_id': agent_id,
            'connector_cls': connector_cls if connector_cls else self._connector_cls,
            'perceptors': perceptors,
            'actuators': actuators,
            'll_reasoners': ll_reasoners,
            'learners': learners,
            'knowledge': knowledge,
            'hl_reasoners': hl_reasoners,
            'goal_graphs': goal_graphs,
            'memory': memory,
            'connector_kwargs': connector_kwargs if connector_kwargs else self._connector_kwargs,
            'step_frequency': self._step_frequency if step_frequency is None else step_frequency,
            'status_frequency': self._status_frequency if status_frequency is None else status_frequency,
            'control_frequency': self._control_frequency if control_frequency is None else control_frequency,
            'exec_start_time': self._exec_start_time if exec_start_time is None else exec_start_time,
            'start_delay': start_delay,
            'exec_duration': self._exec_duration_sec if exec_duration is None else exec_duration,
            'save_dir': f'/{self.SAVE_SUBDIR}',
            'save_format': self._save_format,
            'resume': self._resume if resume is None else resume,
            'log_level': self._log_level if log_level is None else log_level,
            'log_format': self._log_format,
            'status_msg_format': self._status_msg_format
        }

        if requirements_path is not None:
            kwargs['requirements_path'] = str(requirements_path)

        self._agents[agent_id] = AgentEntry(
            agent_id=agent_id,
            port_mapping=port_mapping if port_mapping else self._port_mapping,
            num_copies=num_copies,
            kwargs=kwargs,
            save_logs=save_logs if save_logs is not None else self._save_logs,
            tags=tags
        )
        if self._task_group is not None:
            self._task_group.create_task(self._run_agent(self._agents[agent_id], force_run=self._force_run))

    def _compose_directory(self) -> Directory:
        if self._environment is not None:
            directory = Directory(self._environment.address, self._environment.tags)
        else:
            directory = Directory()

        host, port = self._mas_rmq_uri_internal.split(':')

        for agent in self._agents.values():
            directory.external.add_agent(
                agent_id=agent.agent_id,
                address={
                    'exchange_name': self._mas_rmq_exchange_name,
                    'agent_id': agent.agent_id,
                    'host': host,
                    'port': port
                },
                tags=agent.tags
            )

        return directory

    def _docker_build_base(self,
                           mhagenta_version: str = 'latest',
                           local_build: PathLike | None = None,
                           prerelease: bool = False
                           ) -> None:
        if not mhagenta_version:
            mhagenta_version = CONTAINER_VERSION
        try:
            print(f'===== PULLING RABBITMQ BASE IMAGE: {REPO}:rmq =====')
            self._docker_client.images.pull(REPO, tag='rmq')
        except docker.errors.ImageNotFound:
            print('Pulling failed...')
            print(f'===== BUILDING RABBITMQ BASE IMAGE: {REPO}:rmq =====')
            if self._rabbitmq_image is None:
                self._rabbitmq_image, _ = (
                    self._docker_client.images.build(path=RABBIT_IMG_PATH,
                                                     tag=f'{REPO}:rmq',
                                                     rm=True,
                                                     quiet=False
                                                     ))

        if self._base_image is None:
            print(f'===== LOOKING FOR AGENT BASE IMAGE: {REPO}:{mhagenta_version} =====')
            try:
                self._base_image = self._docker_client.images.list(name=f'{REPO}:{mhagenta_version}')[0]
            except IndexError:
                print('\tIMAGE NOT FOUND LOCALLY...')
                if local_build is None:
                    print(f'===== PULLING AGENT BASE IMAGE: {REPO}:{mhagenta_version} =====')
                    try:
                        self._base_image = self._docker_client.images.pull(REPO, mhagenta_version)
                        print('\tSUCCESSFULLY PULLED THE IMAGE!')
                        return
                    except docker.errors.ImageNotFound:
                        print('\tPULLING AGENT BASE IMAGE FAILED...')
                build_dir = self._save_dir.resolve() / 'tmp' / 'mha-base'
                try:
                    print(f'===== BUILDING AGENT BASE IMAGE: {REPO}:{mhagenta_version} =====')
                    shutil.copytree(BASE_IMG_PATH, build_dir, dirs_exist_ok=True)
                    if local_build is not None:
                        local_build = Path(local_build).resolve()
                        shutil.copytree(local_build / 'mhagenta', build_dir / 'mha-local' / 'mhagenta')
                        shutil.copy(local_build / 'pyproject.toml', build_dir / 'mha-local' / 'pyproject.toml')
                        shutil.copy(local_build / 'README.md', build_dir / 'mha-local' / 'README.md')
                    else:
                        (build_dir / 'mha-local').mkdir(parents=True, exist_ok=True)
                    self._base_image, _ = (
                        self._docker_client.images.build(
                            path=str(build_dir),
                            buildargs={
                                'SRC_IMAGE': REPO,
                                'SRC_TAG': 'rmq',
                                'PRE_VERSION': "true" if prerelease else "false",
                                'LOCAL': "false" if local_build is None else "true",
                            },
                            tag=f'{REPO}:{mhagenta_version}',
                            rm=True,
                            quiet=False
                        ))
                except Exception as ex:
                    shutil.rmtree(build_dir, ignore_errors=True)
                    raise ex
                shutil.rmtree(build_dir)

    def _docker_build_agent(self,
                            agent: AgentEntry,
                            rebuild_image: bool = True,
                            ) -> None:
        if rebuild_image:
            try:
                img = self._docker_client.images.list(name=f'mhagent:{agent.agent_id}')[0]
                img.remove(force=True)
            except IndexError:
                pass
        print(f'===== BUILDING AGENT IMAGE: mhagent:{agent.agent_id} =====')
        agent_dir = self._save_dir.resolve() / agent.agent_id
        if self._force_run and agent_dir.exists():
            shutil.rmtree(agent_dir)

        (agent_dir / 'out/').mkdir(parents=True)
        agent.dir = agent_dir
        agent.save_dir = agent_dir / 'out' / 'save'

        build_dir = agent_dir / 'tmp/'
        shutil.copytree(AGENT_IMG_PATH, build_dir.resolve())
        (build_dir / 'src').mkdir(parents=True, exist_ok=True)
        shutil.copy(Path(mhagenta.core.__file__).parent.resolve() / 'agent_launcher.py', (build_dir / 'src' / 'agent_launcher.py').resolve())
        shutil.copy(Path(mhagenta.__file__).parent.resolve() / 'scripts' / 'start.sh', (build_dir / 'src' / 'start.sh').resolve())

        agent.kwargs['directory'] = self._compose_directory()

        if agent.kwargs['exec_start_time'] is None:
            agent.kwargs['exec_start_time'] = self._start_time

        agent.kwargs['exec_start_time'] += self._agent_start_delay

        end_estimate = agent.kwargs['exec_start_time'] + agent.kwargs['start_delay'] + agent.kwargs['exec_duration']
        if self._simulation_end_ts < end_estimate:
            self._simulation_end_ts = end_estimate

        if 'requirements_path' in agent.kwargs:
            requirements_path = agent.kwargs.pop('requirements_path')
            shutil.copy(requirements_path, (build_dir / 'src' / 'requirements.txt').resolve())

        with open((build_dir / 'src' / 'agent_params').resolve(), 'wb') as f:
            dill.dump(agent.kwargs, f, recurse=True)

        base_tag = self._base_image.tags[0].split(':')
        agent.image, _ = self._docker_client.images.build(path=str(build_dir.resolve()),
                                                          buildargs={
                                                              'SRC_IMAGE': base_tag[0],
                                                              'SRC_VERSION': base_tag[1]
                                                          },
                                                          tag=f'mhagent:{agent.agent_id}',
                                                          rm=True,
                                                          quiet=False
                                                          )
        shutil.rmtree(build_dir)

    async def _run_agent(self,
                         agent: AgentEntry,
                         force_run: bool = False
                         ) -> None:
        if agent.num_copies == 1:
            print(f'===== RUNNING AGENT IMAGE \"mhagent:{agent.agent_id}\" AS CONTAINER \"{agent.agent_id}\" =====')
        else:
            print(f'===== RUNNING AGENT IMAGE \"mhagent:{agent.agent_id}\" AS '
                  f'{agent.num_copies} CONTAINERS \"{agent.agent_id}_#\" =====')
        for i in range(agent.num_copies):
            if agent.num_copies == 1:
                agent_name = agent.agent_id
                agent_dir = (agent.dir / "out").resolve()
            else:
                agent_name = f'{agent.agent_id}_{i}'
                agent_dir = (agent.dir / str(i) / "out").resolve()

            agent_dir.mkdir(parents=True, exist_ok=True)
            try:
                container = self._docker_client.containers.get(agent_name)
                if force_run:
                    container.remove(force=True)
                else:
                    raise NameError(f'Container {agent_name} already exists')
            except NotFound:
                pass

            agent.container = self._docker_client.containers.run(
                image=agent.image,
                detach=True,
                name=agent_name,
                environment={"AGENT_ID": agent_name},
                volumes={
                    str(agent_dir): {'bind': '/out', 'mode': 'rw'}
                },
                extra_hosts={'host.docker.internal': 'host-gateway'},
                ports=agent.port_mapping
            )

    async def arun(self,
                   mhagenta_version: str = 'latest',
                   force_run: bool = False,
                   gui: bool = False,
                   rebuild_agents: bool = True,
                   local_build: PathLike | None = None,
                   prerelease: bool = False
                   ) -> None:
        """Run all the agents as an async method. Use in case you want to control the async task loop yourself.

        Args:
            mhagenta_version (str, optional): Version of mhagenta base container. Defaults to 'latest'.
            force_run (bool, optional, default=False): In case containers with some of the specified agent IDs exist,
                specify whether to force remove the old container to run the new ones. Otherwise, an exception will be
                raised.
            gui (bool, optional, default=False): Specifies whether to open the log monitoring window for the
                orchestrator.
            rebuild_agents (bool, optional, default=True): Whether to rebuild the agents. Defaults to True.
            local_build (PathLike, optional): Specifies the path to a local build of MHAgentA (as opposed to the latest
                one from PyPI) to be used for building agents.
            prerelease (bool, optional, default=False): Specifies whether to allow agents to use the latest prerelease
                version of mhagenta while building the container.

        Raises:
            NameError: Raised if a container for one of the specified agent IDs already exists and `force_run` is False.

        """

        self._start_time = time.time()
        if self._base_image is None:
            self._docker_build_base(mhagenta_version=mhagenta_version, local_build=local_build, prerelease=prerelease)

        self._force_run = force_run
        for agent in self._agents.values():
            self._docker_build_agent(agent, rebuild_image=rebuild_agents)

        if gui:
            self._monitor = Monitor()

        self._running = True

        self.start_rabbitmq()

        if self._environment is not None:
            self._environment.environment['exec_duration'] -= (time.time() - self._start_time)
            env_param_path = (self._environment.dir / 'params').resolve()
            with open(env_param_path, 'wb') as f:
                dill.dump(self._environment.environment, f, recurse=True)
            self._environment.process = subprocess.Popen([
                    f'{Path(sys.executable).resolve()}',
                    f'{(Path(__file__).parent.parent / "environment" / "environment_launcher.py").resolve()}',
                    str(env_param_path)
                ],
                stdout=None,
            )
            if not self._agents:
                self._simulation_end_ts = time.time() + self._exec_duration_sec + self._agent_start_delay
        async with asyncio.TaskGroup() as tg:
            self._task_group = tg
            if gui:
                tg.create_task(self._monitor.run())
            # if self._environment is not None:
            #     tg.create_task(self._read_logs())
            tg.create_task(self._simulation_end_timer())
            for agent in self._agents.values():
                tg.create_task(self._run_agent(agent, force_run=force_run))
                tg.create_task(self._read_logs(agent, gui))
        self._running = False
        for agent in self._agents.values():
            agent.container.remove()
        if self._environment is not None:
            print('Waiting for the environment process to stop gracefully...')
            try:
                self._environment.process.wait(20.)
            except subprocess.TimeoutExpired:
                print('Killing the environment process...')
                self._environment.process.kill()
        if self._mas_rmq_container is not None and self._mas_rmq_close_on_exit:
            try:
                self._mas_rmq_container.stop()
            except Exception:
                pass
        print('===== EXECUTION FINISHED =====')

    def run(self,
            mhagenta_version='latest',
            force_run: bool = False,
            gui: bool = False,
            rebuild_agents: bool = True,
            local_build: PathLike | None = None,
            prerelease: bool = False
            ) -> None:
        """Run all the agents.

        Args:
            mhagenta_version (str, optional): Version of mhagenta base container. Defaults to 'latest'.
            force_run (bool, optional, default=False): In case containers with some of the specified agent IDs exist,
                specify whether to force remove the old container to run the new ones. Otherwise, an exception will be
                raised.
            gui (bool, optional, default=False): Specifies whether to open the log monitoring window for the
                orchestrator.
            rebuild_agents (bool, optional, default=True): Whether to rebuild the agents. Defaults to True.
            local_build (PathLike, optional): Specifies the path to a local build of MHAgentA (as opposed to the latest
                one from PyPI) to be used for building agents.
            prerelease (bool, optional, default=False): Specifies whether to allow agents to use the latest prerelease
                version of mhagenta while building the container.

        Raises:
            NameError: Raised if a container for one of the specified agent IDs already exists and `force_run` is False.

        """
        asyncio.run(self.arun(
            mhagenta_version=mhagenta_version,
            force_run=force_run,
            gui=gui,
            rebuild_agents=rebuild_agents,
            local_build=local_build,
            prerelease=prerelease
        ))

    @staticmethod
    def _agent_stopped(agent: AgentEntry) -> bool:
        agent.container.reload()
        return agent.container.status == 'exited'

    @property
    def _agents_stopped(self) -> bool:
        if self._all_stopped:
            return True
        for agent in self._agents.values():
            if not self._agent_stopped(agent):
                return False
        self._all_stopped = True
        return True

    async def _simulation_end_timer(self) -> None:
        await asyncio.sleep(self._simulation_end_ts - time.time())
        self._stopping = True

    def _add_log(self, log: str | bytes, gui: bool = False, file_stream: TextIOWrapper | None = None) -> None:
        if isinstance(log, bytes):
            log = log.decode().strip('\n\r')
        print(log)
        if gui:
            self._monitor.add_log(log)
        if file_stream is not None:
            file_stream.write(f'{log}\n')
            file_stream.flush()

    async def _read_logs(self, agent: AgentEntry, gui: bool = False) -> None:
        logs = self._docker_client.containers.get(agent.container.id).logs(stdout=True, stderr=True, stream=True, follow=True)
        if gui:
            module_ids = agent.module_ids
            module_ids.insert(0, 'root')
            self._monitor.add_agent(agent.agent_id, module_ids)

        if self._save_logs:
            f = open(self._save_dir / f'{agent.agent_id}.log', 'w')
        else:
            f = None
        while True:
            if self._stopping and self._agents_stopped:
                if f is not None:
                    f.close()
                break
            for line in logs:
                self._add_log(line, gui=gui, file_stream=f)
                await asyncio.sleep(0)
            await asyncio.sleep(self.LOG_CHECK_FREQ)

    def __getitem__(self, agent_id: str) -> AgentEntry:
        return self._agents[agent_id]

    def start_rabbitmq(self) -> None:
        self._connect_rabbitmq()

    def _connect_rabbitmq(self) -> None:
        if self._mas_rmq_uri_internal is None:
            return
        try:
            host, port = self._mas_rmq_uri.split(':') if ':' in self._mas_rmq_uri_internal else (self._mas_rmq_uri_internal, 5672)
            connection = BlockingConnection(pika.ConnectionParameters(host, port))
            connection.close()
        except AMQPConnectionError:
            self._mas_rmq_container = self._docker_client.containers.run(
                image=DEFAULT_RMQ_IMAGE,
                detach=True,
                name='mhagenta-rmq',
                ports={
                    '5672': 5672,
                    '15672':15672
                },
                remove=True,
                tty=True
            )



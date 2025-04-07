from __future__ import annotations

import logging
from logging import Logger
from typing import Optional, Tuple, Any

import yaml

import docker
import docker.errors

from netunicorn.base.architecture import Architecture
from netunicorn.base.deployment import Deployment
from netunicorn.base.environment_definitions import DockerImage
from netunicorn.base.nodes import CountableNodePool, Node, Nodes
from returns.result import Failure, Result, Success

from netunicorn.director.base.connectors.protocol import (
    NetunicornConnectorProtocol,
)
from netunicorn.director.base.connectors.types import StopExecutorRequest


class DockerConnector(NetunicornConnectorProtocol):
    def __init__(
            self,
            connector_name: str,
            configuration: str | None,
            netunicorn_gateway: str,
            logger: Optional[Logger] = None
    ):
        self.connector_name = connector_name

        if configuration is None:
            self.base_url = 'unix://var/run/docker.sock'
            self.default_network = None
            self.access_tags = []
        else:
            with open(configuration, 'r') as f:
                config = yaml.safe_load(f)
            self.base_url = config['netunicorn.docker.base_url']
            self.default_network = config.get('netunicorn.docker.default_network', None)
            self.access_tags = config.get('netunicorn.docker.access.tags', [])

        self.client = docker.DockerClient(base_url=self.base_url)
        self.netunicorn_gateway = netunicorn_gateway
        self.logger = logger or logging.getLogger(__name__)
        self.nodename = 'dockerhost'

        version = self.client.version()
        assert version['Os'] == 'linux'
        self.architecture = Architecture.UNKNOWN
        if version['Arch'] == 'amd64':
            self.architecture = Architecture.LINUX_AMD64
        elif version['Arch'] in {'aarch64', 'arm64'}:
            self.architecture = Architecture.LINUX_ARM64
        else:
            self.logger.warning(f"Unknown architecture: {version['Arch']}")

        self.logger.debug(
            f"Initialized DockerConnector with base_url={self.base_url}, nodename={self.nodename}, architecture={self.architecture}")

    async def initialize(self, *args: Any, **kwargs: Any) -> None:
        pass

    async def health(self, *args: Any, **kwargs: Any) -> Tuple[bool, str]:
        try:
            self.client.ping()
            self.logger.debug('DockerConnector is healthy')
            return True, 'OK'
        except Exception as e:
            self.logger.exception(e)
            return False, str(e)

    async def shutdown(self, *args: Any, **kwargs: Any) -> None:
        pass

    async def get_nodes(
            self,
            username: str,
            authentication_context: Optional[dict[str, str]] = None,
            *args: Any,
            **kwargs: Any,
    ) -> Nodes:
        pool = CountableNodePool([
            Node(
                name=self.nodename,
                properties={
                    "netunicorn-environments": {"DockerImage"},
                    "netunicorn-access-tags": self.access_tags,
                },
                architecture=self.architecture
            )
        ])
        self.logger.debug(f"Returning nodes: {pool}")
        return pool

    async def deploy(
            self,
            username: str,
            experiment_id: str,
            deployments: list[Deployment],
            deployment_context: Optional[dict[str, str]],
            authentication_context: Optional[dict[str, str]] = None,
            *args: Any,
            **kwargs: Any,
    ) -> dict[str, Result[Optional[str], str]]:
        results = {}
        for deployment in deployments:
            if not isinstance(deployment.environment_definition, DockerImage):
                self.logger.debug(f"Received unexpected environment definition: {deployment.environment_definition}")
                results[deployment.executor_id] = Failure(
                    f"Supports only docker images, but received {deployment.environment_definition}")
                continue

            try:
                self.client.images.pull(deployment.environment_definition.image)
                results[deployment.executor_id] = Success(None)
                self.logger.debug(f"Image {deployment.environment_definition.image} pulled")
            except Exception as e:
                self.logger.exception(e)
                results[deployment.executor_id] = Failure(str(e))
        return results

    @staticmethod
    def _extract_volumes_args(arguments: list[str]) -> list[str]:
        # legacy format: "/host/path:/container/path"
        legacy_volumes = [x for x in arguments if x.startswith("/") and ":" in x]

        # normal docker format: "-v /host/path:/container/path:ro"
        docker_volumes = []
        for element in (x for x in arguments if x.startswith("-v") or x.startswith("--volume")):
            mapping = element.split(' ')
            if len(mapping) > 1:
                mapping = mapping[1].split(':')
                if len(mapping) >= 2:
                    docker_volumes.append(f"{mapping[0]}:{mapping[1]}")

        return legacy_volumes + docker_volumes

    async def execute(
            self,
            username: str,
            experiment_id: str,
            deployments: list[Deployment],
            execution_context: Optional[dict[str, str]],
            authentication_context: Optional[dict[str, str]] = None,
            *args: Any,
            **kwargs: Any,
    ) -> dict[str, Result[Optional[str], str]]:

        result = {}
        for deployment in deployments:
            if not deployment.prepared:
                result[deployment.executor_id] = Failure("The deployment is not prepared")
                self.logger.debug(f"Received not prepared deployment: {deployment}")
                continue
            if not isinstance(deployment.environment_definition, DockerImage):
                result[deployment.executor_id] = Failure(
                    f"Supports only docker images, but received {deployment.environment_definition}")
                self.logger.debug(f"Received unexpected environment definition: {deployment.environment_definition}")
                continue

            if not deployment.node.name == self.nodename:
                result[deployment.executor_id] = Failure(f"Received unexpected nodename: {deployment.node.name}")
                self.logger.warning(f"Received unexpected nodename: {deployment.node.name}")
                continue

            ports = {}
            for x, y in deployment.environment_definition.runtime_context.ports_mapping.items():
                ports[f'{x}/tcp'] = y
                ports[f'{x}/udp'] = y

            envvars = deployment.environment_definition.runtime_context.environment_variables
            envvars['NETUNICORN_GATEWAY_ENDPOINT'] = self.netunicorn_gateway
            envvars['NETUNICORN_EXECUTOR_ID'] = deployment.executor_id
            envvars['NETUNICORN_EXPERIMENT_ID'] = experiment_id

            volumes = []
            add_args = deployment.environment_definition.runtime_context.additional_arguments
            if add_args:
                volumes = self._extract_volumes_args(add_args)

            self.logger.debug(
                f"Starting container {deployment.executor_id} with image {deployment.environment_definition.image} "
                f"and environment variables {envvars} and volumes {volumes}"
            )

            try:
                self.client.containers.run(
                    image=deployment.environment_definition.image,
                    detach=True,
                    tty=False,
                    environment=envvars,
                    network=deployment.environment_definition.runtime_context.network or self.default_network,
                    ports=ports,
                    remove=True,
                    auto_remove=True,
                    name=deployment.executor_id,
                    volumes=volumes,
                )
                result[deployment.executor_id] = Success(None)
            except Exception as e:
                self.logger.exception(e)
                result[deployment.executor_id] = Failure(str(e))
        return result

    async def stop_executors(
            self,
            username: str,
            requests_list: list[StopExecutorRequest],
            cancellation_context: Optional[dict[str, str]],
            authentication_context: Optional[dict[str, str]] = None,
            *args: Any,
            **kwargs: Any,
    ) -> dict[str, Result[Optional[str], str]]:
        result = {}
        for request in requests_list:
            if not request['node_name'] == self.nodename:
                result[request['executor_id']] = Failure(f"Received unexpected nodename: {request['node_name']}")
                self.logger.warning(f"Received unexpected nodename: {request['node_name']}")
                continue

            try:
                container = self.client.containers.get(request['executor_id'])
                container.stop()
                result[request['executor_id']] = Success("The container was stopped")
                self.logger.debug(f"Stopped container {request['executor_id']}")
            except docker.errors.NotFound:
                result[request['executor_id']] = Success("The container was not found")
                self.logger.debug(f"Container {request['executor_id']} was not found")
            except Exception as e:
                result[request['executor_id']] = Failure(str(e))
                self.logger.exception(e)

        return result

    async def cleanup(
            self,
            experiment_id: str,
            deployments: list[Deployment],
            *args: Any,
            **kwargs: Any
    ) -> None:
        # stop containers if they are still working
        for deployment in deployments:
            try:
                container = self.client.containers.get(deployment.executor_id)
                container.stop()
                self.logger.debug(f"Stopped container {deployment.executor_id}")
            except docker.errors.NotFound:
                pass
            except Exception as e:
                self.logger.exception(e)

        # remove images
        for deployment in deployments:
            try:
                self.client.images.remove(deployment.environment_definition.image)
                self.logger.debug(f"Removed image {deployment.environment_definition.image}")
            except docker.errors.ImageNotFound:
                self.logger.debug(f"Image {deployment.environment_definition.image} was not found")
            except Exception as e:
                self.logger.exception(e)


async def test_main():
    from netunicorn.base.pipeline import Pipeline
    import uuid

    logger = logging.getLogger('test-logger')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())

    connector = DockerConnector(
        connector_name='test',
        configuration=None,
        netunicorn_gateway='dummy',
        logger=logger
    )
    print(await connector.health())
    nodes = await connector.get_nodes('test')
    for node in nodes:
        print(node.name, node.architecture, node.properties)

    deployment = Deployment(
        node=nodes[0],
        pipeline=Pipeline()
    )
    deployment.executor_id = uuid.uuid4()
    deployment.prepared = True
    deployment.environment_definition = DockerImage()
    deployment.environment_definition.image = 'hello-world'
    deployment.environment_definition.runtime_context.ports_mapping = {8000: 8000}
    deployment.environment_definition.runtime_context.environment_variables = {'TEST': 'test'}

    print(await connector.deploy('test', 'test', [deployment], None))
    print(await connector.execute('test', 'test', [deployment], None))


if __name__ == '__main__':
    import asyncio

    asyncio.run(test_main())

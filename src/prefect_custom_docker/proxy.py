"""
a thin wrapper which spins up docker containers which run ETL jobs:
"""
import logging
import os

import docker
from prefect import flow
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

logging.basicConfig(format='[%(threadName)s] %(asctime)s %(levelname)s: %(message)s', level=logging.INFO)


class DockerContainerProxyConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="", case_sensitive=True)

    # Required environment variables
    image: str = Field(alias="IMAGE")
    command: None | str = Field(alias="COMMAND", default=None)
    volumes: None | list[str] = Field(alias="VOLUMES", default=None)

    # Optional dynamic environment mapping
    environment: dict[str, str] = Field(default_factory=dict)

    def __init__(self, **data):
        super().__init__(**data)

        # Collect all env vars ending with `_ENV`
        env_dict = {}
        for key, value in os.environ.items():
            if key.endswith("_ENV"):
                # strip the suffix or keep as-is; here we keep the raw key
                env_dict[key] = value

        # Inject into settings
        object.__setattr__(self, "environment", env_dict)


def run_docker_container(config: DockerContainerProxyConfig):
    logging.info("starting a custom Docker container flow")

    client = docker.from_env()
    logging.info(f"creating docker container for image={config.image} with volumes={config.volumes}")
    container_logs = client.containers.run(
        image=config.image,
        command=config.command,
        volumes=config.volumes,
        environment=config.environment,
        remove=True
    )
    for line in container_logs.splitlines():
        print(line.decode("utf-8"))


@flow(log_prints=True)
def docker_flow():
    try:
        config = DockerContainerProxyConfig()
        logging.info(f"successfully loaded docker proxy config: {config.image} ...")
        run_docker_container(config)
    except Exception as e:
        print("Encountered error: ", e)


if __name__ == '__main__':
    docker_flow()
import os

import pytest

from prefect_custom_docker.proxy import DockerContainerProxyConfig, docker_flow, run_docker_container


def test_should_load_proxy_settings():
    # mandatory
    os.environ.setdefault("IMAGE", "ubuntu")
    os.environ.setdefault("VOLUMES", "[\"/foo:/bar\",\"/opt:/opt\"]")

    # optional environment dictionary
    os.environ.setdefault("FOO_ENV", "12345")

    candidate = DockerContainerProxyConfig()
    assert candidate.image == "ubuntu"
    assert candidate.volumes == ["/foo:/bar", "/opt:/opt"]
    assert candidate.environment.get("FOO_ENV") == "12345"

def test_should_spin_up_docker_container():
    os.environ.setdefault("DOCKER_HOST", "unix://var/run/docker.sock") # use local docker provider
    os.environ.setdefault("IMAGE", "ubuntu")
    os.environ.setdefault("COMMAND", "echo hello world")

    try:
        config = DockerContainerProxyConfig()
        run_docker_container(config)
    except Exception as e:
        pytest.fail(f"failed to spin up Docker container: {e}")
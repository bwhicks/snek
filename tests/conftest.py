import socket
from random import randint
from typing import Callable, Union, Generator
import docker
from docker.models.containers import Container
import pytest


class TestVaultException(Exception):
    pass


def get_open_port() -> Union[int, Callable]:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        port = randint(9000, 30000)
        if sock.connect_ex(("localhost", port)):
            return port
        return get_open_port()


@pytest.fixture
def test_vault() -> Generator[Container, None, None]:
    client = docker.from_env()
    test_container = client.containers.run(
        "vault", detach=True, ports={8200: get_open_port()}
    )
    if isinstance(test_container, Container):
        yield test_container
        test_container.stop()
        test_container.remove()
    else:
        raise TestVaultException(test_container)
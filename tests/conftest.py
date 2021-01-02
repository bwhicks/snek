import logging
import socket
from random import randint
from time import sleep
from typing import Callable, Generator, Tuple, Union

import docker
import pytest
import requests
from docker.models.containers import Container
from snek.client import VaultClient

logger = logging.getLogger(__name__)


class TestVaultException(Exception):
    """An exception when creating Docker container with test Vault."""

    pass


def get_open_port() -> Union[int, Callable]:
    """Find an open port and return it or recurse until one is found."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        port = randint(9000, 30000)
        if sock.connect_ex(("localhost", port)):
            return port
        return get_open_port()


@pytest.fixture(scope="session")
def vault_conn() -> Generator[Tuple[int, str], None, None]:
    """Return port and token of a Dockerized dev vault server."""
    client = docker.from_env()
    port = get_open_port()
    token = "devtoken"
    test_container = client.containers.run(
        "vault",
        detach=True,
        ports={8200: port},
        environment={"VAULT_DEV_ROOT_TOKEN_ID": token},
    )

    # This is really dumb but quickest way to tell vault is answering
    # requests.
    up = False
    retries = 5
    while not up or not retries:
        try:
            requests.get(f"http://localhost:{port}/v1/sys/init")
            up = True
        except IOError:
            sleep(0.01)
            retries -= 1
            continue

    if not retries:
        raise TestVaultException("Test Vault failed to start.")

    yield port, token
    test_container.stop()
    test_container.remove()


@pytest.fixture
def test_vault(vault_conn):
    port, token = vault_conn
    yield vault_conn
    requests.delete(
        f"http://localhost:{port}/v1/secret/metadata/foo/bar",
        headers={"X-Vault-Token": token},
    )


@pytest.fixture
def test_client(test_vault):
    port, token = test_vault
    return VaultClient(f"http://localhost:{port}/", token)


@pytest.fixture
def mock_http_call(mocker):
    mock_request = mocker.patch("snek.client.requests.Session.request")
    mock_request.return_value.json.return_value = {}
    return mock_request

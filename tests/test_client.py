import pytest
from snek.client import VaultClient
from snek.constants import HttpStatusCode


@pytest.mark.vault
def test_get(test_vault):
    port, token = test_vault
    client = VaultClient(f"http://localhost:{port}/", token)
    res = client.get("/v1/sys/init", params={"X-Vault-Token": None})
    assert res.status_code == HttpStatusCode.SUCCESS_DATA.value
    assert res.json()["initialized"] is True

import pytest


@pytest.mark.vault
def test_vault_fixture(test_vault):
    port, token = test_vault
    assert isinstance(port, int)
    assert isinstance(token, str)

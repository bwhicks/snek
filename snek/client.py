import requests

from snek.constants import HttpMethod


class VaultClient:
    """Client for low-level HTTP communications with Vault API."""

    def __init__(self, vault_addr: str, token: str, extra_headers=None):
        if extra_headers is None:
            extra_headers = {}
        extra_headers["X-Vault-Token"] = token
        extra_headers["Content-Type"] = "application/json"

        self.session = requests.Session()
        self.vault_addr = vault_addr
        self.session.headers.update(extra_headers)

    def _make_request(self, method, path, **kwargs):
        return self.session.request(method, path, **kwargs)

    def get(self, api_path, params=None):
        return self._make_request(HttpMethod.GET.value, self.)
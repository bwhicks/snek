from typing import Dict, Optional
from urllib.parse import urljoin

import requests

from snek.constants import HttpMethod


class VaultClient:
    """Client for low-level HTTP communications with Vault API."""

    def __init__(
        self,
        vault_addr: str,
        token: str,
        extra_headers: Optional[Dict[str, str]] = None,
    ):
        if extra_headers is None:
            extra_headers = {}
        extra_headers["X-Vault-Token"] = token
        extra_headers["Content-Type"] = "application/json"

        self.session = requests.Session()
        self.vault_addr = vault_addr
        self.session.headers.update(extra_headers)

    def _make_request(
        self, method: str, path: str, **kwargs
    ) -> Optional[requests.Response]:
        """Internal method to make requests."""
        try:
            return self.session.request(method, path, **kwargs)
        except IOError:
            return None

    def get(
        self, api_path: str, params: Optional[Dict[str, str]] = None
    ) -> Optional[requests.Response]:
        """Make a GET request to the appropriate API path."""
        return self._make_request(
            HttpMethod.GET.value, urljoin(self.vault_addr, api_path)
        )

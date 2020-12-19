import json
import logging
from typing import Any, Dict, Optional
from urllib.parse import urljoin

import requests

from snek.constants import HttpMethod, HttpStatusCode

logger = logging.getLogger(__name__)


class VaultClient:
    """Client for low-level HTTP communications with Vault API."""

    def __init__(
        self,
        vault_addr: str,
        token: str,
        namespace: Optional[str] = None,
        extra_headers: Optional[Dict[str, str]] = None,
    ):
        if extra_headers is None:
            extra_headers = {}

        extra_headers["X-Vault-Token"] = token
        extra_headers["Content-Type"] = "application/json"
        if namespace:
            extra_headers["X-Vault-Namespace"] = namespace

        self.session = requests.Session()
        self.vault_addr = vault_addr
        self.session.headers.update(extra_headers)

    @staticmethod
    def _get_text(res: requests.Response) -> str:
        try:
            return json.dumps(res.json())
        except json.JSONDecodeError:
            return res.text

    def make_request(
        self, method: str, path: str, **kwargs
    ) -> Optional[requests.Response]:
        """Internal method to make requests."""
        try:
            res = self.session.request(method, path, **kwargs)
        except IOError:
            logging.exception("Connection to Vault failed.")
            return None
        if HttpStatusCode(res.status_code) not in [
            HttpStatusCode.SUCCESS_DATA,
            HttpStatusCode.SUCCESS_NO_DATA,
            HttpStatusCode.HEALTH_PERFORMANCE_STANDBY_NODE,
            HttpStatusCode.HEALTH_STANDBY_NODE,
        ]:
            text = self._get_text(res)
            logger.error(f"{res.status_code}: {text}")
            return None

        return res

    def get(
        self, api_path: str, params: Optional[Dict[str, str]] = None
    ) -> Optional[requests.Response]:
        """Make a GET request to the appropriate API path."""
        return self.make_request(
            HttpMethod.GET.value, urljoin(self.vault_addr, api_path), params=params
        )

    def put(
        self, api_path: str, data: Optional[Dict[str, Any]] = None
    ) -> Optional[requests.Response]:
        """Make a PUT request to the given API path."""
        return self.make_request(
            HttpMethod.PUT.value, urljoin(self.vault_addr, api_path), json=data
        )

    def post(
        self, api_path: str, data: Optional[Dict[str, Any]] = None
    ) -> Optional[requests.Response]:
        """Make a HEAD request to the given API path."""
        return self.make_request(
            HttpMethod.POST.value, urljoin(self.vault_addr, api_path), json=data
        )

    def list(
        self, api_path: str, params: Optional[Dict[str, str]] = None
    ) -> Optional[requests.Response]:
        """Make a LIST request to the given API path."""
        return self.make_request(
            HttpMethod.LIST.value, urljoin(self.vault_addr, api_path), params=params
        )

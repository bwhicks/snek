import json
from typing import Any, Dict, Optional

from .client import VaultClient
from .exceptions import (
    KV2SecretException,
    SecretCreateUpdateException,
    SecretReadException,
    VaultClientException,
)
from .models import VaultResponse


class KVSecretV2:
    """Representation of a secret returned from the KV2 engine"""

    #: Vault path
    path: str
    #: version (if given)
    version: Optional[int]
    #: raw response from Vault for secret path
    vault_response: Optional[VaultResponse]

    def __init__(
        self,
        path: str,
        version: Optional[int] = None,
        vault_response: Optional[VaultResponse] = None,
    ):
        if vault_response is not None:
            self.vault_response = vault_response
            self.data = vault_response.response["data"]
        else:
            self.data = None
        self.path = path
        self.version = version

    @property
    def value(self) -> Dict[str, Any]:
        """Value of the secret."""
        return self.data["data"] if "data" in self.data else None

    def __str__(self) -> str:
        return f"{self.path}: {json.dumps(self.data)}"


class KVSecretV2API:
    """Instance configured with a client to connect to the KV2 secrets engine."""

    def __init__(self, client: VaultClient, mount_path: str = "secret"):

        self.client = client
        self.mount_path = f"/v1/{mount_path}"
        self.base_path = f"{self.mount_path}/data"
        self.base_metadata_path = f"{self.mount_path}/metadata"

    def configure(
        self,
        max_versions: int = 0,
        cas_required: bool = False,
        delete_version_after: str = "0s",
    ) -> VaultResponse:
        configuration = {
            "max_versions": max_versions,
            "cas_required": cas_required,
            "delete_version_after": delete_version_after,
        }
        try:
            return self.client.post(f"{self.mount_path}/config", data=configuration)
        except VaultClientException:
            raise KV2SecretException("Failed to configure KV-V2 engine.")

    def read(self, path: str, version: Optional[int] = None) -> Optional[KVSecretV2]:
        """Get a secret at a given path.

        Raises:
            SecretGetException: Raised if secret not found at path.
        """
        try:
            res = self.client.get(
                f"{self.base_path}/{path}",
                params={"version": str(version) if version is not None else version},
            )
            return KVSecretV2(vault_response=res, path=path)
        except VaultClientException:
            raise SecretReadException(
                f"Failed to read secrets at {self.base_path}/{path}"
            )

    def create_or_update(
        self,
        path: str,
        data: Dict[str, Any],
        cas: Optional[int] = None,
    ) -> KVSecretV2:
        """Create or update a secret at a path.

        Raises:
            SecretCreateUpdateException: Raised when secret cannot be created at path.
        """
        payload = {"data": data, "options": {}}
        if cas is not None:
            payload["options"] = {"cas": cas}
        try:
            res = self.client.post(f"{self.base_path}/{path}", data=payload)
            return KVSecretV2(path=path, vault_response=res)
        except VaultClientException:
            raise SecretCreateUpdateException(
                f"Failed to create or update secret at {self.base_path}/{path}"
            )

from typing import Any, Dict, List, Optional, Union

from .constants import HttpStatusCode


class VaultResponse:
    """Base wrapper class for responses from Vault."""

    def __init__(
        self,
        response: Dict[str, Any],
        status_code: Union[HttpStatusCode, int],
        errors: Optional[List[str]] = None,
    ):
        self.response = response
        if isinstance(status_code, HttpStatusCode):
            self.status_code = status_code
        else:
            self.status_code = HttpStatusCode(status_code)
        self.errors = errors

    @property
    def ok(self) -> bool:
        """Return whether status errors exist."""
        return self.status_code in [
            HttpStatusCode.SUCCESS_DATA,
            HttpStatusCode.SUCCESS_NO_DATA,
            HttpStatusCode.HEALTH_PERFORMANCE_STANDBY_NODE,
            HttpStatusCode.HEALTH_STANDBY_NODE,
        ]

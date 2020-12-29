from typing import Optional

from .constants import HttpStatusCode


class SnekException(Exception):
    """Base class for errors raised by the snek module."""

    pass


class VaultClientException(SnekException):
    """Error with client communication."""

    def __init__(self, message: str, status_code: Optional[HttpStatusCode] = None):
        self.message = message
        self.status_code = status_code


class KV2SecretExceptiont(SnekException):
    """Base exception for KV2 secret errors."""


class SecretCreateUpdateException(SnekException):
    """Error creating or updating a secret."""

    pass


class SecretReadException(SnekException):
    """Error getting a secret."""

    pass


class UnboundModelError(SnekException):
    """Raised when a model is not bound to an API and a method is called that
    requires this."""

    pass

from enum import Enum


class HttpMethod(Enum):
    """HTTP method constants."""

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    HEAD = "HEAD"


class HttpStatusCode(Enum):
    """Human readable status codes for conventions used in Vault v1 API."""

    SUCCESS_DATA = 200
    SUCCESS_NO_DATA = 204
    INVALID_REQUEST = 400
    FORBIDDEN = 403
    INVALID_PATH = 404
    HEALTH_STANDBY_NODE = 429
    HEALTH_PERFORMANCE_STANDBY_NODE = 473
    INTERNAL_SERVER_ERROR = 500
    THIRD_PARTY_ERROR = 502
    VAULT_MAINTENANCE = 503

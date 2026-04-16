from __future__ import annotations

from typing import Any

from beehivehub.constants import BEEHIVE_DOCS


class BeehiveHubError(Exception):
    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        code: str | None = None,
    ) -> None:
        self.message = message
        self.status_code = status_code
        self.code = code
        full_message = f"{message} — Docs: {BEEHIVE_DOCS}"
        super().__init__(full_message)

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": type(self).__name__,
            "message": str(self),
            "status_code": self.status_code,
            "code": self.code,
        }


class BeehiveHubAPIError(BeehiveHubError):
    def __init__(
        self,
        message: str,
        status_code: int,
        code: str | None = None,
        body: Any = None,
    ) -> None:
        super().__init__(message, status_code=status_code, code=code)
        self.body = body

    def to_dict(self) -> dict[str, Any]:
        data = super().to_dict()
        data["body"] = self.body
        return data


class BeehiveHubAuthenticationError(BeehiveHubError):
    def __init__(self, message: str) -> None:
        super().__init__(message, status_code=401, code="authentication_error")


class BeehiveHubValidationError(BeehiveHubError):
    def __init__(self, message: str, details: Any = None) -> None:
        super().__init__(message, status_code=400, code="validation_error")
        self.details = details

    def to_dict(self) -> dict[str, Any]:
        data = super().to_dict()
        data["details"] = self.details
        return data


class BeehiveHubNotFoundError(BeehiveHubError):
    def __init__(self, resource: str = "Resource") -> None:
        super().__init__(f"{resource} not found", status_code=404, code="not_found")
        self.resource = resource

    def to_dict(self) -> dict[str, Any]:
        data = super().to_dict()
        data["resource"] = self.resource
        return data


class BeehiveHubRateLimitError(BeehiveHubError):
    def __init__(self, message: str) -> None:
        super().__init__(message, status_code=429, code="rate_limit_error")


class BeehiveHubNetworkError(BeehiveHubError):
    def __init__(self, message: str) -> None:
        super().__init__(message, status_code=None, code="network_error")

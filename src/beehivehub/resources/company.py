"""Company resource."""

from __future__ import annotations

from typing import Any

from beehivehub.requests import RequestFunction


class Company:
    """Operations on company data.

    Args:
        request: Configured HTTP request function.
    """

    def __init__(self, request: RequestFunction) -> None:
        self._request = request

    def get(self) -> Any:
        """Get the company data.

        Returns:
            The company object.
        """
        return self._request("/company", method="GET")

    def update(self, data: dict[str, Any]) -> Any:
        """Update the company data.

        Args:
            data: Company payload (use UpdateCompanyData.model_dump(exclude_none=True)).

        Returns:
            The updated company object.
        """
        return self._request("/company", method="PUT", data=data)

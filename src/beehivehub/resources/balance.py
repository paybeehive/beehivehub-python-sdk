"""Balance resource."""

from __future__ import annotations

from typing import Any

from beehivehub.requests import RequestFunction


class Balance:
    """Operations on account balance.

    Args:
        request: Configured HTTP request function.
    """

    def __init__(self, request: RequestFunction) -> None:
        self._request = request

    def get(self) -> Any:
        """Get the available account balance.

        Returns:
            The balance object with amount in cents.
        """
        return self._request("/balance/available", method="GET")

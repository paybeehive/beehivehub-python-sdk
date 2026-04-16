"""Transfers resource."""

from __future__ import annotations

from typing import Any

from beehivehub.requests import RequestFunction


class Transfers:
    """Operations on transfers.

    Args:
        request: Configured HTTP request function.
    """

    def __init__(self, request: RequestFunction) -> None:
        self._request = request

    def create(self, data: dict[str, Any]) -> Any:
        """Create a transfer to a recipient.

        Args:
            data: Transfer payload (use CreateTransferData.model_dump(exclude_none=True)).

        Returns:
            The created transfer object.
        """
        return self._request("/transfers", method="POST", data=data)

    def get(self, id: int) -> Any:
        """Get a transfer by ID.

        Args:
            id: Transfer ID.

        Returns:
            The transfer object.
        """
        return self._request(f"/transfers/{id}", method="GET")

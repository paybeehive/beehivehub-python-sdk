"""Recipients resource."""

from __future__ import annotations

from typing import Any

from beehivehub.requests import RequestFunction


class Recipients:
    """Operations on recipients.

    Args:
        request: Configured HTTP request function.
    """

    def __init__(self, request: RequestFunction) -> None:
        self._request = request

    def create(self, data: dict[str, Any]) -> Any:
        """Create a new recipient.

        Args:
            data: Recipient payload (use CreateRecipientData.model_dump(exclude_none=True)).

        Returns:
            The created recipient object.
        """
        return self._request("/recipients", method="POST", data=data)

    def list(self) -> Any:
        """List all recipients.

        Returns:
            A list of recipient objects.
        """
        return self._request("/recipients", method="GET")

    def get(self, id: int) -> Any:
        """Get a recipient by ID.

        Args:
            id: Recipient ID.

        Returns:
            The recipient object.
        """
        return self._request(f"/recipients/{id}", method="GET")

    def update(self, id: int, data: dict[str, Any]) -> Any:
        """Update a recipient.

        Args:
            id: Recipient ID.
            data: Recipient payload (use UpdateRecipientData.model_dump(exclude_none=True)).

        Returns:
            The updated recipient object.
        """
        return self._request(f"/recipients/{id}", method="PUT", data=data)

"""Customers resource."""

from __future__ import annotations

from typing import Any

from beehivehub.requests import RequestFunction


class Customers:
    """Operations on customers.

    Args:
        request: Configured HTTP request function.
    """

    def __init__(self, request: RequestFunction) -> None:
        self._request = request

    def create(self, data: dict[str, Any]) -> Any:
        """Create a new customer.

        Args:
            data: Customer payload (use CreateCustomerData.model_dump(exclude_none=True)).

        Returns:
            The created customer object.
        """
        return self._request("/customers", method="POST", data=data)

    def list(self, params: dict[str, str]) -> Any:
        """List customers by email.

        Args:
            params: Query parameters. Must include "email".

        Returns:
            A list of customer objects.
        """
        return self._request("/customers", method="GET", params=params)

    def get(self, id: int) -> Any:
        """Get a customer by ID.

        Args:
            id: Customer ID.

        Returns:
            The customer object.
        """
        return self._request(f"/customers/{id}", method="GET")

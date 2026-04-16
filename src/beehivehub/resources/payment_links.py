"""Payment links resource."""

from __future__ import annotations

from typing import Any

from beehivehub.constants import PAYMENT_LINK_URL_PRODUCTION, PAYMENT_LINK_URL_SANDBOX
from beehivehub.requests import RequestFunction
from beehivehub.utils import generate_alias


class PaymentLinks:
    """Operations on payment links.

    Includes special behaviors:
    - Auto-generates alias if missing or empty on create/update.
    - Injects a ``url`` field into every response that contains an alias.

    Args:
        request: Configured HTTP request function.
        environment: API environment — "production" or "sandbox".
    """

    def __init__(self, request: RequestFunction, environment: str = "production") -> None:
        self._request = request
        self._link_base_url = (
            PAYMENT_LINK_URL_SANDBOX if environment == "sandbox" else PAYMENT_LINK_URL_PRODUCTION
        )

    def _with_url(self, data: dict[str, Any]) -> dict[str, Any]:
        """Add the ``url`` field if the response contains a truthy alias."""
        alias = data.get("alias")
        if not alias:
            return data
        return {**data, "url": f"{self._link_base_url}/{alias}"}

    @staticmethod
    def _ensure_alias(data: dict[str, Any]) -> dict[str, Any]:
        """Generate an alias if it is missing or empty."""
        alias = data.get("alias")
        if alias is None or (isinstance(alias, str) and alias.strip() == ""):
            data = {**data, "alias": generate_alias()}
        return data

    def create(self, data: dict[str, Any]) -> Any:
        """Create a payment link.

        Generates an alias automatically if omitted or empty. The returned
        object includes a ``url`` field built from the alias.

        Args:
            data: Payment link payload (use CreatePaymentLinkData.model_dump(exclude_none=True)).

        Returns:
            The created payment link object with ``url`` injected.
        """
        data = self._ensure_alias(data)
        result = self._request("/payment-links", method="POST", data=data)
        return self._with_url(result)

    def list(self) -> Any:
        """List all payment links.

        Each item with an alias gets a ``url`` field injected.

        Returns:
            A list of payment link objects.
        """
        results = self._request("/payment-links", method="GET")
        if isinstance(results, list):
            return [self._with_url(item) for item in results]
        return results

    def get(self, id: int) -> Any:
        """Get a payment link by ID.

        Args:
            id: Payment link ID.

        Returns:
            The payment link object with ``url`` injected.
        """
        result = self._request(f"/payment-links/{id}", method="GET")
        return self._with_url(result)

    def update(self, id: int, data: dict[str, Any]) -> Any:
        """Update a payment link.

        Generates an alias automatically if omitted or empty. The returned
        object includes a ``url`` field built from the alias.

        Args:
            id: Payment link ID.
            data: Payment link payload (use UpdatePaymentLinkData.model_dump(exclude_none=True)).

        Returns:
            The updated payment link object with ``url`` injected.
        """
        data = self._ensure_alias(data)
        result = self._request(f"/payment-links/{id}", method="PUT", data=data)
        return self._with_url(result)

    def delete(self, id: int) -> None:
        """Delete a payment link.

        Args:
            id: Payment link ID.
        """
        self._request(f"/payment-links/{id}", method="DELETE")

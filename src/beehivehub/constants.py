import base64
from importlib.metadata import PackageNotFoundError, version

BASE_URL_PRODUCTION = "https://api.conta.paybeehive.com.br/v1"
BASE_URL_SANDBOX = "https://api.sandbox.hopysplit.com.br/v1"

PAYMENT_LINK_URL_PRODUCTION = "https://link.conta.paybeehive.com.br"
PAYMENT_LINK_URL_SANDBOX = "https://link.sandbox.hopysplit.com.br"

BEEHIVE_DOCS = "https://docs.beehivehub.io/"

try:
    SDK_VERSION = version("beehivehub-python-sdk")
except PackageNotFoundError:
    SDK_VERSION = "0.0.0-dev"


def default_headers(api_key: str) -> dict[str, str]:
    credentials = base64.b64encode(f"{api_key}:x".encode()).decode()
    return {
        "Authorization": f"Basic {credentials}",
        "Content-Type": "application/json",
        "User-Agent": f"Beehive Hub Python SDK ({SDK_VERSION})",
    }

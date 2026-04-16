"""Utility functions for the BeeHive Hub SDK."""

import random
import string


def generate_alias() -> str:
    """Generate a random 10-character alphanumeric alias.

    Returns:
        A string of 10 characters from [a-zA-Z0-9].
    """
    charset = string.ascii_letters + string.digits
    return "".join(random.choices(charset, k=10))

"""Tests for utils module."""

import re

from beehivehub.utils import generate_alias


class TestGenerateAlias:
    def test_returns_10_characters(self):
        alias = generate_alias()
        assert len(alias) == 10

    def test_only_alphanumeric_characters(self):
        alias = generate_alias()
        assert re.match(r"^[a-zA-Z0-9]{10}$", alias)

    def test_generates_different_values(self):
        aliases = {generate_alias() for _ in range(100)}
        assert len(aliases) > 1

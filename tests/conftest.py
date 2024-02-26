#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Copyright (C) 2019-2024, AllWorldIT.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# type: ignore

"""Testing stuff."""

import re

import pytest

__all__ = ["Helpers", "CustomPytestRegex"]

# Make sure basetests has its asserts rewritten
pytest.register_assert_rewrite("tests.basetests")


#
# Helpers
#


class Helpers:
    """Helpers for our tests."""

    @staticmethod
    def pytest_regex(pattern: str, flags: int = 0):
        """Regex test for pytest."""
        return CustomPytestRegex(pattern, flags)

    @staticmethod
    def bird_since_field():
        """Return our 'since' field match."""
        return CustomPytestRegex(r"[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}")


class CustomPytestRegex:
    """Assert that a given string meets some expectations."""

    def __init__(self, pattern, flags=0):
        """Inititalize object."""
        self._regex = re.compile(pattern, flags)

    def __eq__(self, actual):
        """Check if the 'actual' string matches the regex."""
        return bool(self._regex.match(actual))

    def __repr__(self):
        """Return our representation."""
        return self._regex.pattern


@pytest.fixture()
def helpers():
    """Return our helpers."""
    return Helpers


@pytest.fixture(name="testpath")
def fixture_testpath(request):
    """Test file path."""
    return str(request.node.fspath)

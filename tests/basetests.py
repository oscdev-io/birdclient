#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Copyright (C) 2019-2020, AllWorldIT.
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
# pylint: disable=import-error,too-few-public-methods

"""Test base class for BirdClient."""

import os.path
from typing import List

__all__ = ["BirdClientTestBaseCase"]


class BirdClientTestBaseCase:
    """Test the BirdClient class."""

    def load_test_data(self, testpath: str, filename: str) -> List[str]:
        """Read in a file and return the lines."""
        testdir = os.path.dirname(testpath)
        with open(f"{testdir}/{filename}", "r", encoding="UTF-8") as datafile:
            data = datafile.read()
        return data.splitlines()

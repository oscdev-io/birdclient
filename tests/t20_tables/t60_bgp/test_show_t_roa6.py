#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Copyright (C) 2019-2025, AllWorldIT.
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

"""Tests for the Python BirdClient class."""

from birdclient import BirdClient

from ...basetests import BirdClientTestBaseCase

__all__ = ["TestBirdClientShowTROA6"]


class TestBirdClientShowTROA6(BirdClientTestBaseCase):
    """Test the BirdClient class."""

    def test_show_t_roa6(self, testpath: str) -> None:
        """Test show t_roa6 table."""

        birdclient = BirdClient()
        result = birdclient.show_route_table("t_roa6", self.load_test_data(testpath, "test_show_t_roa6.txt"))

        correct_result = {
            "fc00:101::/48": [
                {
                    "ROA.asn": "65001",
                    "ROA.max": 48,
                    "bestpath": True,
                    "pref": 200,
                    "protocol": "rpki6",
                    "since": "2024-04-30 04:51:38",
                    "type": ["static", "univ"],
                }
            ]
        }

        assert result == correct_result, "The show_route_table() result does not match what it should be"

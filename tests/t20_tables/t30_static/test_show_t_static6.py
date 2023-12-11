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

"""Tests for the Python BirdClient class."""

from birdclient import BirdClient

from ...basetests import BirdClientTestBaseCase

__all__ = ["TestBirdClientShowTStatic6"]


class TestBirdClientShowTStatic6(BirdClientTestBaseCase):
    """Test the BirdClient class."""

    def test_show_t_static6(self, testpath: str) -> None:
        """Test show static6 table."""

        birdclient = BirdClient()
        result = birdclient.show_route_table("t_static6", self.load_test_data(testpath, "test_show_t_static6.txt"))

        correct_result = {
            "fec0:10::/64": [
                {
                    "bestpath": True,
                    "nexthops": [{"gateway": "fec0::4", "interface": "eth0"}],
                    "pref": 200,
                    "prefix_type": "unicast",
                    "protocol": "static6",
                    "since": "2019-09-01 13:36:14",
                    "type": ["static", "univ"],
                }
            ],
            "fec0:20::/64": [
                {
                    "bestpath": True,
                    "nexthops": [{"gateway": "fec0::5", "interface": "eth0"}],
                    "pref": 200,
                    "prefix_type": "unicast",
                    "protocol": "static6",
                    "since": "2019-09-01 13:36:14",
                    "type": ["static", "univ"],
                }
            ],
        }

        assert result == correct_result, "The show_route_table() result does not match what it should be"

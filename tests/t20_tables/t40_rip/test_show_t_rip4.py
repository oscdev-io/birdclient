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

__all__ = ["TestBirdClientShowTRIP4"]


class TestBirdClientShowTRIP4(BirdClientTestBaseCase):
    """Test the BirdClient class."""

    def test_show_t_rip4(self, testpath: str) -> None:
        """Test show RIP4 table."""

        birdclient = BirdClient()
        result = birdclient.show_route_table("t_rip4", self.load_test_data(testpath, "test_show_t_rip4.txt"))

        correct_result = {
            "192.168.10.0/24": [
                {
                    "bestpath": False,
                    "metric1": 3,
                    "nexthops": [{"gateway": "192.168.0.1", "interface": "eth0"}],
                    "pref": 120,
                    "prefix_type": "unicast",
                    "protocol": "rip4",
                    "since": "2019-10-01 17:59:41",
                }
            ],
            "192.168.21.0/24": [
                {
                    "bestpath": True,
                    "nexthops": [{"gateway": "192.168.20.3", "interface": "eth1"}],
                    "pref": 200,
                    "prefix_type": "unicast",
                    "protocol": "static4",
                    "since": "2019-10-01 17:59:38",
                }
            ],
        }

        assert result == correct_result, "The show_route_table() result does not match what it should be"

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

__all__ = ["TestBirdClientShowTStatic4v3"]


class TestBirdClientShowTStatic4v3(BirdClientTestBaseCase):
    """Test the BirdClient class."""

    def test_show_t_static4v3(self, testpath: str) -> None:
        """Test show static4 table."""

        birdclient = BirdClient()
        result = birdclient.show_route_table("t_static4", self.load_test_data(testpath, "test_show_t_static4v3.txt"))

        correct_result = {
            "10.0.1.0/24": [
                {
                    "attributes": {
                        "preference": 200,
                        "source": "static",
                    },
                    "bestpath": True,
                    "nexthops": [
                        {
                            "gateway": "192.168.0.4",
                            "interface": "eth1",
                        },
                    ],
                    "pref": 200,
                    "prefix_type": "unicast",
                    "protocol": "static4",
                    "since": "2025-02-21 07:30:51",
                },
            ],
        }

        assert result == correct_result, "The show_route_table() result does not match what it should be"

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

__all__ = ["TestBirdClientShowTBGP4b"]


class TestBirdClientShowTBGP4b(BirdClientTestBaseCase):
    """Test the BirdClient class."""

    def test_show_t_bgp4(self, testpath: str) -> None:
        """Test show BGP4 table."""

        birdclient = BirdClient()
        result = birdclient.show_route_table("t_bgp4", self.load_test_data(testpath, "test_show_t_bgp4v3b.txt"))

        correct_result = {
            "100.64.101.0/24": [
                {
                    "attributes": {
                        "bgp_large_community": [
                            (
                                65000,
                                3,
                                1,
                            ),
                        ],
                        "bgp_local_pref": 100,
                        "bgp_next_hop": [
                            "100.64.0.2",
                        ],
                        "bgp_origin": "IGP",
                        "bgp_path": [],
                        "from": "100.64.0.2",
                        "hostentry": "via 100.64.0.2 table master4",
                        "igp_metric": 0,
                        "preference": 100,
                        "source": "BGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "nexthops": [
                        {
                            "gateway": "100.64.0.2",
                            "interface": "eth0",
                        },
                    ],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp4_AS65000_e1",
                    "since": "2025-02-22 08:23:11",
                },
            ],
        }

        assert result == correct_result, "The show_route_table() result does not match what it should be"

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

__all__ = ["TestBirdClientShowTOSPF4v3"]


class TestBirdClientShowTOSPF4v3(BirdClientTestBaseCase):
    """Test the BirdClient class."""

    def test_show_t_ospf4(self, testpath: str) -> None:
        """Test show OSPF4 table."""

        birdclient = BirdClient()
        result = birdclient.show_route_table("t_ospf4", self.load_test_data(testpath, "test_show_t_ospf4v3.txt"))

        correct_result = {
            "10.0.0.0/24": [
                {
                    "attributes": {
                        "preference": 200,
                        "source": "static",
                    },
                    "bestpath": True,
                    "nexthops": [
                        {
                            "gateway": "100.101.0.2",
                            "interface": "eth1",
                        },
                    ],
                    "pref": 200,
                    "prefix_type": "unicast",
                    "protocol": "static4",
                    "since": "2025-02-21 17:48:44",
                },
            ],
            "100.64.0.0/24": [
                {
                    "attributes": {
                        "ospf_metric1": 10,
                        "ospf_router_id": "0.0.0.2",
                        "preference": 150,
                        "source": "OSPF",
                    },
                    "bestpath": True,
                    "metric1": 10,
                    "nexthops": [
                        {
                            "interface": "eth0",
                        },
                    ],
                    "ospf_type": "I",
                    "pref": 150,
                    "prefix_type": "unicast",
                    "protocol": "ospf4",
                    "router_id": "0.0.0.2",
                    "since": "2025-02-21 17:48:49",
                },
            ],
        }

        assert result == correct_result, "The show_route_table() result does not match what it should be"

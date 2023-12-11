#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Copyright (C) 2019-2023, AllWorldIT.
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

__all__ = ["TestBirdClientShowTOSPF62"]


class TestBirdClientShowTOSPF62(BirdClientTestBaseCase):
    """Test the BirdClient class."""

    def test_show_t_ospf6_2(self, testpath: str) -> None:
        """Test show OSPF6 table."""

        birdclient = BirdClient()
        result = birdclient.show_route_table("t_ospf6", self.load_test_data(testpath, "test_show_t_ospf6_2.txt"))

        correct_result = {
            "fc00:90::/64": [
                {
                    "attributes": {
                        "OSPF.metric1": 40,
                        "OSPF.metric2": 10000,
                        "OSPF.router_id": "100.64.10.2",
                        "OSPF.tag": "0x00000000",
                    },
                    "bestpath": False,
                    "metric1": 40,
                    "metric2": 10000,
                    "nexthops": [
                        {"gateway": "fe80::20:1ff:fe00:1", "interface": "eth0", "weight": 1},
                        {"gateway": "fe80::20:1ff:fe02:1", "interface": "eth0", "weight": 1},
                    ],
                    "ospf_type": "E2",
                    "pref": 150,
                    "prefix_type": "unicast",
                    "protocol": "ospf6",
                    "router_id": "100.64.10.2",
                    "since": "2019-09-30 17:14:13",
                    "type": ["OSPF-E2", "univ"],
                }
            ],
            "fc50::2/127": [
                {
                    "attributes": {"OSPF.metric1": 40, "OSPF.router_id": "100.64.10.2"},
                    "bestpath": False,
                    "metric1": 40,
                    "nexthops": [
                        {"gateway": "fe80::20:1ff:fe00:1", "interface": "eth0", "weight": 1},
                        {"gateway": "fe80::20:1ff:fe02:1", "interface": "eth0", "weight": 1},
                    ],
                    "ospf_type": "I",
                    "pref": 150,
                    "prefix_type": "unicast",
                    "protocol": "ospf6",
                    "router_id": "100.64.10.2",
                    "since": "2019-09-30 17:14:13",
                    "type": ["OSPF", "univ"],
                }
            ],
            "fec0:20::/64": [
                {
                    "bestpath": False,
                    "metric1": 20,
                    "metric2": 10000,
                    "nexthops": [{"gateway": "fe80::8c84:28ff:fe6c:40ae", "interface": "eth0"}],
                    "ospf_type": "E2",
                    "pref": 150,
                    "prefix_type": "unicast",
                    "protocol": "ospf6",
                    "router_id": "172.16.10.1",
                    "since": "2019-09-01 14:20:00",
                    "type": ["OSPF-E2", "univ"],
                }
            ],
            "fec0::/64": [
                {
                    "bestpath": False,
                    "metric1": 20,
                    "nexthops": [{"gateway": "fe80::8c84:28ff:fe6c:40ae", "interface": "eth0"}],
                    "ospf_type": "I",
                    "pref": 150,
                    "prefix_type": "unicast",
                    "protocol": "ospf6",
                    "router_id": "172.16.10.1",
                    "since": "2019-09-01 14:19:58",
                    "type": ["OSPF", "univ"],
                }
            ],
        }

        assert result == correct_result, "The show_route_table() result does not match what it should be"

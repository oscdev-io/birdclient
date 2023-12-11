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

__all__ = ["TestBirdClientShowTOSPF4"]


class TestBirdClientShowTOSPF4(BirdClientTestBaseCase):
    """Test the BirdClient class."""

    def test_show_t_ospf4(self, testpath: str) -> None:  # noqa: CFQ001
        """Test show OSPF4 table."""

        birdclient = BirdClient()
        result = birdclient.show_route_table("t_ospf4", self.load_test_data(testpath, "test_show_t_ospf4.txt"))

        correct_result = {
            "10.0.1.0/24": [
                {
                    "bestpath": True,
                    "nexthops": [{"gateway": "192.168.0.4", "interface": "eth0"}],
                    "pref": 200,
                    "prefix_type": "unicast",
                    "protocol": "static4",
                    "since": "2019-09-01 13:36:14",
                    "type": ["static", "univ"],
                }
            ],
            "10.0.2.0/24": [
                {
                    "bestpath": True,
                    "nexthops": [{"gateway": "192.168.0.5", "interface": "eth0"}],
                    "pref": 200,
                    "prefix_type": "unicast",
                    "protocol": "static4",
                    "since": "2019-09-01 13:36:14",
                    "type": ["static", "univ"],
                }
            ],
            "100.64.43.2/31": [
                {
                    "attributes": {"OSPF.metric1": 20, "OSPF.router_id": "100.64.20.1"},
                    "bestpath": False,
                    "metric1": 20,
                    "nexthops": [{"gateway": "100.64.20.1", "interface": "eth0"}],
                    "ospf_type": "I",
                    "pref": 150,
                    "prefix_type": "unicast",
                    "protocol": "ospf4",
                    "router_id": "100.64.20.1",
                    "since": "2019-09-30 17:14:09",
                    "type": ["OSPF", "univ"],
                }
            ],
            "100.64.44.2/31": [
                {
                    "attributes": {"OSPF.metric1": 30, "OSPF.router_id": "100.64.30.1"},
                    "bestpath": True,
                    "metric1": 20,
                    "nexthops": [{"gateway": "100.64.30.1", "interface": "eth0"}],
                    "ospf_type": "I",
                    "pref": 150,
                    "prefix_type": "unicast",
                    "protocol": "ospf4",
                    "router_id": "100.64.30.1",
                    "since": "2019-09-30 17:14:09",
                    "type": ["OSPF", "univ"],
                }
            ],
            "100.64.50.2/31": [
                {
                    "attributes": {"OSPF.metric1": 40, "OSPF.router_id": "100.64.10.2"},
                    "bestpath": False,
                    "metric1": 40,
                    "nexthops": [
                        {"gateway": "100.64.20.1", "interface": "eth0", "weight": 1},
                        {"gateway": "100.64.20.5", "interface": "eth0", "weight": 1},
                    ],
                    "ospf_type": "I",
                    "pref": 150,
                    "prefix_type": "unicast",
                    "protocol": "ospf4",
                    "router_id": "100.64.10.2",
                    "since": "2019-09-30 17:14:13",
                    "type": ["OSPF", "univ"],
                }
            ],
            "100.90.0.0/28": [
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
                        {"gateway": "100.64.20.1", "interface": "eth0", "weight": 1},
                        {"gateway": "100.64.20.5", "interface": "eth0", "weight": 1},
                    ],
                    "ospf_type": "E2",
                    "pref": 150,
                    "prefix_type": "unicast",
                    "protocol": "ospf4",
                    "router_id": "100.64.10.2",
                    "since": "2019-09-30 17:14:13",
                    "type": ["OSPF-E2", "univ"],
                }
            ],
            "172.16.100.0/24": [
                {
                    "bestpath": False,
                    "nexthops": [{"gateway": "172.16.10.10", "interface": "eth9"}],
                    "pref": 10,
                    "prefix_type": "unicast",
                    "protocol": "kernel4",
                    "since": "2019-09-01 13:36:14",
                    "type": ["inherit", "univ"],
                }
            ],
        }

        assert result == correct_result, "The show_route_table() result does not match what it should be"

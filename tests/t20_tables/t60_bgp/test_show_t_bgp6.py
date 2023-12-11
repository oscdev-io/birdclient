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

__all__ = ["TestBirdClientShowTBGP6"]


class TestBirdClientShowTBGP6(BirdClientTestBaseCase):
    """Test the BirdClient class."""

    def test_show_t_bgp6(self, testpath: str) -> None:  # noqa: CFQ001
        """Test show BGP6 table."""

        birdclient = BirdClient()
        result = birdclient.show_route_table("t_bgp6", self.load_test_data(testpath, "test_show_t_bgp6.txt"))

        correct_result = {
            "fc00:130::/48": [
                {
                    "asn": "AS65007",
                    "attributes": {
                        "BGP.as_path": [65007],
                        "BGP.large_community": [
                            (65000, 4, 65414),
                            (65007, 3, 1),
                            (65000, 3, 2),
                            (65000, 1, 901),
                        ],
                        "BGP.local_pref": 750,
                        "BGP.next_hop": ["fc61::3", "fe80::61:1ff:fe00:1"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "nexthops": [{"gateway": "fc61::3", "interface": "eth1"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp_AS65007_client3_peer6",
                    "since": "2019-09-30 17:14:00",
                    "type": ["BGP", "univ"],
                },
                {
                    "attributes": {
                        "BGP.as_path": [],
                        "BGP.cluster_list": "0.0.0.1",
                        "BGP.large_community": [(65000, 3, 1)],
                        "BGP.local_pref": 940,
                        "BGP.next_hop": ["fc50::5"],
                        "BGP.origin": "IGP",
                        "BGP.originator_id": "100.64.10.2",
                    },
                    "bestpath": False,
                    "bgp_type": "i",
                    "from": "fc20::3",
                    "nexthops": [
                        {"gateway": "fe80::20:1ff:fe00:1", "interface": "eth0", "weight": 1},
                        {"gateway": "fe80::20:1ff:fe02:1", "interface": "eth0", "weight": 1},
                    ],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp_AS65000_rr2_peer6",
                    "since": "2019-09-30 17:14:20",
                    "type": ["BGP", "univ"],
                },
            ],
            "fc20::/64": [
                {
                    "attributes": {
                        "BGP.as_path": [],
                        "BGP.cluster_list": "0.0.0.1",
                        "BGP.community": [
                            (1, 0),
                            (1, 1),
                            (1, 2),
                        ],
                        "BGP.ext_community": [("rt", 1, 1), ("ro", 2, 2)],
                        "BGP.large_community": [(65000, 3, 1)],
                        "BGP.local_pref": 930,
                        "BGP.next_hop": ["fc20::1"],
                        "BGP.origin": "IGP",
                        "BGP.originator_id": "100.64.20.1",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "from": "fc10::3",
                    "nexthops": [{"gateway": "fc20::1", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp_AS65000_rr1_peer6",
                    "since": "2019-09-30 17:14:15",
                    "type": ["BGP", "univ"],
                },
                {
                    "asn": "AS65006",
                    "attributes": {
                        "BGP.as_path": [65006],
                        "BGP.cluster_list": "0.0.0.1",
                        "BGP.large_community": [],
                        "BGP.local_pref": 450,
                        "BGP.next_hop": ["fc40::11", "fe80::40:1ff:fe00:1"],
                        "BGP.origin": "IGP",
                        "BGP.originator_id": "100.64.10.1",
                    },
                    "bestpath": False,
                    "bgp_type": "i",
                    "from": "fc20::3",
                    "nexthops": [
                        {"gateway": "fe80::20:1ff:fe00:1", "interface": "eth0", "weight": 1},
                        {"gateway": "fe80::20:1ff:fe02:1", "interface": "eth0", "weight": 1},
                    ],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp_AS65000_rr2_peer6",
                    "since": "2019-09-30 17:14:14",
                    "type": ["BGP", "univ"],
                },
            ],
        }

        assert result == correct_result, "The show_route_table() result does not match what it should be"

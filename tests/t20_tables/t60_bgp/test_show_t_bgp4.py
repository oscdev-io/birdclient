#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Copyright (C) 2019-2024, AllWorldIT.
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

__all__ = ["TestBirdClientShowTBGP4"]


class TestBirdClientShowTBGP4(BirdClientTestBaseCase):
    """Test the BirdClient class."""

    def test_show_t_bgp4(self, testpath: str) -> None:
        """Test show BGP4 table."""

        birdclient = BirdClient()
        result = birdclient.show_route_table("t_bgp4", self.load_test_data(testpath, "test_show_t_bgp4.txt"))

        correct_result = {
            "100.100.0.0/24": [
                {
                    "asn": "AS65001",
                    "attributes": {
                        "BGP.as_path": [65001],
                        "BGP.cluster_list": "0.0.0.1",
                        "BGP.large_community": [],
                        "BGP.local_pref": 750,
                        "BGP.next_hop": ["100.64.50.3"],
                        "BGP.origin": "IGP",
                        "BGP.originator_id": "100.64.10.2",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "from": "100.64.10.3",
                    "nexthops": [
                        {"gateway": "100.64.20.1", "interface": "eth0", "weight": 1},
                        {"gateway": "100.64.20.5", "interface": "eth0", "weight": 1},
                    ],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp_AS65000_rr1_peer4",
                    "since": "2019-09-30 17:14:14",
                    "type": ["BGP", "univ"],
                }
            ],
            "100.201.0.0/24": [
                {
                    "asn": "AS65006",
                    "attributes": {
                        "BGP.as_path": [65006],
                        "BGP.cluster_list": "0.0.0.1",
                        "BGP.large_community": [(65000, 3, 3), (65006, 3, 1)],
                        "BGP.local_pref": 450,
                        "BGP.next_hop": ["100.64.40.11"],
                        "BGP.origin": "IGP",
                        "BGP.originator_id": "100.64.10.1",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "from": "100.64.10.3",
                    "nexthops": [
                        {"gateway": "100.64.20.1", "interface": "eth0", "weight": 1},
                        {"gateway": "100.64.20.5", "interface": "eth0", "weight": 1},
                    ],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp_AS65000_rr1_peer4",
                    "since": "2019-09-30 17:14:14",
                    "type": ["BGP", "univ"],
                },
                {
                    "asn": "AS65004",
                    "attributes": {
                        "BGP.as_path": [65004],
                        "BGP.cluster_list": "0.0.0.1",
                        "BGP.community": [
                            (1, 0),
                            (1, 1),
                            (1, 2),
                        ],
                        "BGP.ext_community": [("rt", 1, 1), ("ro", 2, 2)],
                        "BGP.large_community": [(65000, 3, 4), (65004, 3, 1)],
                        "BGP.local_pref": 150,
                        "BGP.next_hop": ["100.64.43.2"],
                        "BGP.origin": "IGP",
                        "BGP.originator_id": "100.64.20.1",
                    },
                    "bestpath": False,
                    "bgp_type": "i",
                    "from": "100.64.20.3",
                    "nexthops": [{"gateway": "100.64.20.1", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp_AS65000_rr2_peer4",
                    "since": "2019-09-30 17:14:09",
                    "type": ["BGP", "univ"],
                },
            ],
        }

        assert result == correct_result, "The show_route_table() result does not match what it should be"

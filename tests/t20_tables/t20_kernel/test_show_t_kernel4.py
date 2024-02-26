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

__all__ = ["TestBirdClientShowTKernel4"]


class TestBirdClientShowTKernel4(BirdClientTestBaseCase):
    """Test the BirdClient class."""

    def test_show_t_kernel4(self, testpath: str) -> None:
        """Test show kernel4 table."""

        birdclient = BirdClient()
        result = birdclient.show_route_table("t_kernel4", self.load_test_data(testpath, "test_show_t_kernel4.txt"))

        correct_result = {
            "0.0.0.0/0": [
                {
                    "attributes": {
                        "BGP.as_path": [],
                        "BGP.large_community": [(65000, 3, 1)],
                        "BGP.local_pref": 945,
                        "BGP.next_hop": ["192.168.0.5"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "from": "192.168.0.1",
                    "metric": None,
                    "pref": 100,
                    "prefix_type": "unreachable",
                    "protocol": "bgp4_AS65000_r1",
                    "since": "2020-10-07 09:06:05",
                    "type": ["BGP", "univ"],
                }
            ],
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

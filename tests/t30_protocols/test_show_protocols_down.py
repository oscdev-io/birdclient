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

from ..basetests import BirdClientTestBaseCase

__all__ = ["TestBirdClientShowProtocolsDown"]


class TestBirdClientShowProtocolsDown(BirdClientTestBaseCase):
    """Test the BirdClient class."""

    def test_show_protocols_down(self, testpath: str) -> None:
        """Test show protocol for IPv4 when down."""

        birdclient = BirdClient()
        result = birdclient.show_protocols(data=self.load_test_data(testpath, "test_show_protocols_down.txt"))

        correct_result = {
            "bgp4_AS65000_as65000b": {
                "info": "connecting",
                "info_extra": "socket: connection refused",
                "name": "bgp4_AS65000_as65000b",
                "proto": "BGP",
                "since": "2023-12-06 14:26:45",
                "state": "down",
            },
            "bgp4_AS65001_as65001": {
                "info": "waiting",
                "name": "bgp4_AS65001_as65001",
                "proto": "BGP",
                "since": "2023-12-06 14:26:46",
                "state": "down",
            },
            "bgp6_AS65000_as65000b": {
                "info": "connecting",
                "info_extra": "socket: connection refused",
                "name": "bgp6_AS65000_as65000b",
                "proto": "BGP",
                "since": "2023-12-06 14:26:45",
                "state": "down",
            },
            "bgp6_AS65001_as65001": {
                "info": "waiting",
                "name": "bgp6_AS65001_as65001",
                "proto": "BGP",
                "since": "2023-12-06 14:26:46",
                "state": "down",
            },
            "ospf4": {
                "info": "alone",
                "name": "ospf4",
                "proto": "OSPF",
                "since": "2019-09-01 13:13:28",
                "state": "down",
                "table": "t_ospf4",
            },
            "ospf6": {
                "info": "alone",
                "name": "ospf6",
                "proto": "OSPF",
                "since": "2019-09-01 13:13:28",
                "state": "down",
                "table": "t_ospf6",
            },
            "p_ospf4_to_kernel4": {
                "info": "t_ospf4 <=> t_kernel4",
                "name": "p_ospf4_to_kernel4",
                "proto": "Pipe",
                "since": "2019-09-01 13:13:28",
                "state": "up",
            },
            "p_ospf4_to_static4": {
                "info": "t_ospf4 <=> t_static4",
                "name": "p_ospf4_to_static4",
                "proto": "Pipe",
                "since": "2019-09-01 13:13:28",
                "state": "up",
            },
            "p_ospf6_to_kernel6": {
                "info": "t_ospf6 <=> t_kernel6",
                "name": "p_ospf6_to_kernel6",
                "proto": "Pipe",
                "since": "2019-09-01 13:13:28",
                "state": "up",
            },
            "p_ospf6_to_static6": {
                "info": "t_ospf6 <=> t_static6",
                "name": "p_ospf6_to_static6",
                "proto": "Pipe",
                "since": "2019-09-01 13:13:28",
                "state": "up",
            },
            "p_static4_to_kernel4": {
                "info": "t_static4 <=> t_kernel4",
                "name": "p_static4_to_kernel4",
                "proto": "Pipe",
                "since": "2019-09-01 13:13:28",
                "state": "up",
            },
            "p_static6_to_kernel6": {
                "info": "t_static6 <=> t_kernel6",
                "name": "p_static6_to_kernel6",
                "proto": "Pipe",
                "since": "2019-09-01 13:13:28",
                "state": "up",
            },
        }

        assert result == correct_result, "The show_protocol4_down() result does not match what it should be"

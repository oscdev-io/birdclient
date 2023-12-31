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

from ..basetests import BirdClientTestBaseCase

__all__ = ["TestBirdClientShowProtocol6Down"]


class TestBirdClientShowProtocol6Down(BirdClientTestBaseCase):
    """Test the BirdClient class."""

    def test_show_protocol6_down(self, testpath: str) -> None:
        """Test show protocol for IPv6 when down."""

        birdclient = BirdClient()
        result = birdclient.show_protocol("bgp6_AS65000_as65000a", self.load_test_data(testpath, "test_show_protocol6_down.txt"))

        correct_result = {
            "channel": "ipv6",
            "igp_table": "master6",
            "import_limit": 10,
            "import_limit_action": "restart",
            "info": "active",
            "info_extra": "socket: connection refused",
            "input_filter": "f_bgp_AS65000_as65000a_peer_import",
            "last_error": "socket: connection refused",
            "local_as": 65001,
            "name": "bgp6_AS65000_as65000a",
            "neighbor_address": "fc20::1",
            "neighbor_as": 65000,
            "output_filter": "f_bgp_AS65000_as65000a_peer_export",
            "preference": 100,
            "proto": "BGP",
            "since": "2023-12-06 14:26:45",
            "state": "down",
            "table": "t_bgp6_AS65000_as65000a_peer",
        }

        assert result == correct_result, "The show_protocol6_down() result does not match what it should be"

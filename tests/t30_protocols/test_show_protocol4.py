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

__all__ = ["TestBirdClientShowProtocol4"]


class TestBirdClientShowProtocol4(BirdClientTestBaseCase):
    """Test the BirdClient class."""

    def test_show_protocol4(self, testpath: str) -> None:
        """Test show protocol for IPv4."""

        birdclient = BirdClient()
        result = birdclient.show_protocol("bgp4_AS65000_as65000", self.load_test_data(testpath, "test_show_protocol4.txt"))

        correct_result = {
            "bgp_nexthop": "100.64.20.2",
            "channel": "ipv4",
            "igp_table": "master4",
            "import_limit": 400,
            "import_limit_action": "restart",
            "info": "established",
            "input_filter": "f_bgp_AS65000_as65000_peer_import",
            "local_as": 65001,
            "neighbor_address": "100.64.20.1",
            "neighbor_as": 65000,
            "neighbor_id": "100.64.20.1",
            "output_filter": "f_bgp_AS65000_as65000_peer_export",
            "preference": 100,
            "since": "2023-12-04 22:25:36",
            "source_address": "100.64.20.2",
            "routes_exported": 24,
            "routes_imported": 70,
            "state": "up",
            "table": "t_bgp4_AS65000_as65000_peer",
        }

        assert result == correct_result, "The show_protocol4() result does not match what it should be"

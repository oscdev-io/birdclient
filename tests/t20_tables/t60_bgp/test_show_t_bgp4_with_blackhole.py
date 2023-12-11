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

__all__ = ["TestBirdClientShowTBGP4Blackhole"]


class TestBirdClientShowTBGP4Blackhole(BirdClientTestBaseCase):
    """Test the BirdClient class."""

    def test_show_t_bgp4_with_blackhole(self, testpath: str) -> None:
        """Test show BGP4 table with blackhole."""

        birdclient = BirdClient()
        result = birdclient.show_route_table("t_bgp4", self.load_test_data(testpath, "test_show_t_bgp4_with_blackhole.txt"))

        correct_result = {
            "100.64.11.0/24": [
                {
                    "attributes": {"BGP.large_community": [(65000, 3, 1)], "BGP.local_pref": 930},
                    "bestpath": True,
                    "pref": 200,
                    "prefix_type": "blackhole",
                    "protocol": "bgp_originate4",
                    "since": "2019-10-02 11:29:38",
                    "type": ["static", "univ"],
                }
            ]
        }

        assert result == correct_result, "The show_route_table() result does not match what it should be"

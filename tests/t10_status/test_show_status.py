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

"""Show status test for BirdClient."""

from birdclient import BirdClient

from ..basetests import BirdClientTestBaseCase

__all__ = ["TestBirdClientShowStatus"]


class TestBirdClientShowStatus(BirdClientTestBaseCase):
    """Test the BirdClient class."""

    def test_show_status(self, testpath: str) -> None:
        """Test show_status."""

        birdclient = BirdClient()
        result = birdclient.show_status(self.load_test_data(testpath, "test_show_status.txt"))

        correct_result = {
            "last_reboot": "2019-08-15 12:42:47.592",
            "last_reconfiguration": "2019-08-15 12:42:47.592",
            "router_id": "172.16.10.1",
            "server_time": "2019-08-15 12:42:51.638",
            "version": "2.0.4",
        }

        assert result == correct_result, "The show_status() result does not match what it should be"

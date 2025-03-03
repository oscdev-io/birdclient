#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Copyright (C) 2019-2025, AllWorldIT.
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

__all__ = ["TestBirdClientShowTKernel4v3"]


class TestBirdClientShowTKernel4v3(BirdClientTestBaseCase):
    """Test the BirdClient class."""

    def test_show_t_kernel4(self, testpath: str) -> None:  # noqa: CFQ001
        """Test show kernel4 table."""

        birdclient = BirdClient()
        result = birdclient.show_route_table("t_kernel4", self.load_test_data(testpath, "test_show_t_kernel4v3.txt"))

        correct_result = {
            "0.0.0.0/0": [
                {
                    "attributes": {
                        "preference": 200,
                        "source": "static",
                    },
                    "bestpath": True,
                    "nexthops": [
                        {
                            "gateway": "100.201.0.2",
                            "interface": "eth2",
                        },
                    ],
                    "pref": 200,
                    "prefix_type": "unicast",
                    "protocol": "static4",
                    "since": "2025-02-21 09:21:04",
                },
                {
                    "attributes": {
                        "krt_metric": 0,
                        "krt_source": "RTS_DEVICE",
                        "preference": 10,
                        "source": "inherit",
                    },
                    "bestpath": False,
                    "nexthops": [
                        {
                            "gateway": "100.201.0.3",
                            "interface": "eth2",
                        },
                    ],
                    "pref": 10,
                    "prefix_type": "unicast",
                    "protocol": "kernel4",
                    "since": "2025-02-21 09:21:24",
                },
            ],
            "100.121.0.0/24": [
                {
                    "attributes": {
                        "krt_metric": 0,
                        "krt_source": "RTS_DEVICE",
                        "preference": 10,
                        "source": "inherit",
                    },
                    "bestpath": True,
                    "nexthops": [
                        {
                            "gateway": "100.201.0.3",
                            "interface": "eth2",
                        },
                    ],
                    "pref": 10,
                    "prefix_type": "unicast",
                    "protocol": "kernel4",
                    "since": "2025-02-21 09:21:24",
                },
            ],
            "100.122.0.0/24": [
                {
                    "attributes": {
                        "krt_metric": 0,
                        "krt_scope": "link",
                        "krt_source": "RTS_DEVICE",
                        "preference": 10,
                        "source": "inherit",
                    },
                    "bestpath": True,
                    "nexthops": [
                        {
                            "interface": "eth2",
                        },
                    ],
                    "pref": 10,
                    "prefix_type": "unicast",
                    "protocol": "kernel4",
                    "since": "2025-02-21 09:21:24",
                },
            ],
            "100.123.0.0/31": [
                {
                    "attributes": {
                        "krt_metric": 0,
                        "krt_source": "RTS_DEVICE",
                        "preference": 10,
                        "source": "inherit",
                    },
                    "bestpath": True,
                    "pref": 10,
                    "prefix_type": "blackhole",
                    "protocol": "kernel4",
                    "since": "2025-02-21 09:21:24",
                },
            ],
            "100.131.0.0/24": [
                {
                    "attributes": {
                        "preference": 200,
                        "source": "static",
                    },
                    "bestpath": True,
                    "nexthops": [
                        {
                            "gateway": "100.201.0.2",
                            "interface": "eth2",
                        },
                    ],
                    "pref": 200,
                    "prefix_type": "unicast",
                    "protocol": "static4",
                    "since": "2025-02-21 09:21:04",
                },
            ],
            "100.132.0.0/24": [
                {
                    "attributes": {
                        "preference": 200,
                        "source": "static",
                    },
                    "bestpath": True,
                    "nexthops": [
                        {
                            "interface": "eth2",
                        },
                    ],
                    "pref": 200,
                    "prefix_type": "unicast",
                    "protocol": "static4",
                    "since": "2025-02-21 09:21:04",
                },
            ],
            "100.133.0.0/24": [
                {
                    "attributes": {
                        "preference": 200,
                        "source": "static",
                    },
                    "bestpath": True,
                    "pref": 200,
                    "prefix_type": "blackhole",
                    "protocol": "static4",
                    "since": "2025-02-21 09:21:04",
                },
            ],
        }

        assert result == correct_result, "The show_route_table() result does not match what it should be"

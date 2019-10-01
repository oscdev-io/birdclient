"""Tests for the Python BirdClient class."""

import re
from typing import List

from birdclient import BirdClient


class CustomPytestRegex:
    """Assert that a given string meets some expectations."""

    def __init__(self, pattern, flags=0):
        """Inititalize object."""
        self._regex = re.compile(pattern, flags)

    def __eq__(self, actual):
        """Check if the 'actual' string matches the regex."""
        return bool(self._regex.match(actual))

    def __repr__(self):
        """Return our representation."""
        return self._regex.pattern


def since_field():
    """Return our 'since' field match."""
    return CustomPytestRegex(r'[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}')


class TestBirdClient():
    """Test the BirdClient class."""

    def _load_file(self, filename: str) -> List[str]:
        """Read in a file and return the lines."""
        with open(f'tests/{filename}', 'r') as datafile:
            data = datafile.read()
        return data.splitlines()

    def test_show_status(self):
        """Test show_status."""

        birdclient = BirdClient()
        result = birdclient.show_status(self._load_file('test_show_status.txt'))

        correct_result = {
            'last_reboot': '2019-08-15 12:42:47.592',
            'last_reconfiguration': '2019-08-15 12:42:47.592',
            'router_id': '172.16.10.1',
            'server_time': '2019-08-15 12:42:51.638',
            'version': '2.0.4'
        }

        assert result == correct_result, 'The show_status() result does not match what it should be'

    def test_show_protocols(self):
        """Test show_protocols."""

        birdclient = BirdClient()
        result = birdclient.show_protocols(self._load_file('test_show_protocols.txt'))

        correct_result = {
            'ospf4': {
                'info': 'Alone',
                'name': 'ospf4',
                'proto': 'OSPF',
                'since': since_field(),
                'state': 'up',
                'table': 't_ospf4'
            },
            'ospf6': {
                'info': 'Running',
                'name': 'ospf6',
                'proto': 'OSPF',
                'since': since_field(),
                'state': 'up',
                'table': 't_ospf6'
            },
            'p_ospf4_to_kernel4': {
                'info': 't_ospf4 <=> t_kernel4',
                'name': 'p_ospf4_to_kernel4',
                'proto': 'Pipe',
                'since': since_field(),
                'state': 'up',
                'table': '---'
            },
            'p_ospf4_to_static4': {
                'info': 't_ospf4 <=> t_static4',
                'name': 'p_ospf4_to_static4',
                'proto': 'Pipe',
                'since': since_field(),
                'state': 'up',
                'table': '---'
            },
            'p_ospf6_to_kernel6': {
                'info': 't_ospf6 <=> t_kernel6',
                'name': 'p_ospf6_to_kernel6',
                'proto': 'Pipe',
                'since': since_field(),
                'state': 'up',
                'table': '---'
            },
            'p_ospf6_to_static6': {
                'info': 't_ospf6 <=> t_static6',
                'name': 'p_ospf6_to_static6',
                'proto': 'Pipe',
                'since': since_field(),
                'state': 'up',
                'table': '---'
            },
            'p_static4_to_kernel4': {
                'info': 't_static4 <=> t_kernel4',
                'name': 'p_static4_to_kernel4',
                'proto': 'Pipe',
                'since': since_field(),
                'state': 'up',
                'table': '---'
            },
            'p_static6_to_kernel6': {
                'info': 't_static6 <=> t_kernel6',
                'name': 'p_static6_to_kernel6',
                'proto': 'Pipe',
                'since': since_field(),
                'state': 'up',
                'table': '---'
            }
        }

        assert result == correct_result, 'The show_protocols() result does not match what it should be'

    def test_show_route_table_t_static4(self):
        """Test show_route_table."""

        birdclient = BirdClient()
        result = birdclient.show_route_table('t_static4', self._load_file('test_show_route_table_t_static4.txt'))

        correct_result = [
            {
                'prefix': '10.0.1.0/24',
                'primary': '*',
                'proto': 'static4',
                'since': since_field(),
                'type': ['static', 'univ'],
                'weight': '200',
                'nexthops': [{
                    'gateway': '192.168.0.4',
                    'interface': 'eth0',
                    'mpls': None,
                    'onlink': None,
                    'weight': None
                }]
            },
            {
                'prefix': '10.0.2.0/24',
                'primary': '*',
                'proto': 'static4',
                'since': since_field(),
                'type': ['static', 'univ'],
                'weight': '200',
                'nexthops': [{
                    'gateway': '192.168.0.5',
                    'interface': 'eth0',
                    'mpls': None,
                    'onlink': None,
                    'weight': None
                }]
            }
        ]

        assert result == correct_result, 'The show_route_table() result does not match what it should be'

    def test_show_route_table_t_static6(self):
        """Test show_route_table."""

        birdclient = BirdClient()
        result = birdclient.show_route_table('t_static6', self._load_file('test_show_route_table_t_static6.txt'))

        correct_result = [
            {
                'prefix': 'fec0:20::/64',
                'primary': '*',
                'proto': 'static6',
                'since': since_field(),
                'type': ['static', 'univ'],
                'weight': '200',
                'nexthops': [{
                    'gateway': 'fec0::5',
                    'interface': 'eth0',
                    'mpls': None,
                    'onlink': None,
                    'weight': None
                }]
            },
            {
                'prefix': 'fec0:10::/64',
                'primary': '*',
                'proto': 'static6',
                'since': since_field(),
                'type': ['static', 'univ'],
                'weight': '200',
                'nexthops': [{
                    'gateway': 'fec0::4',
                    'interface': 'eth0',
                    'mpls': None,
                    'onlink': None,
                    'weight': None
                }]
            }
        ]

        assert result == correct_result, 'The show_route_table() result does not match what it should be'

    def test_show_route_table_t_kernel4(self):
        """Test show_route_table."""

        birdclient = BirdClient()
        result = birdclient.show_route_table('t_kernel4', self._load_file('test_show_route_table_t_kernel4.txt'))

        correct_result = [
            {
                'prefix': '172.16.100.0/24',
                'primary': None,
                'proto': 'kernel4',
                'since': since_field(),
                'type': ['inherit', 'univ'],
                'weight': '10',
                'nexthops': [{
                    'gateway': '172.16.10.10',
                    'interface': 'eth9',
                    'mpls': None,
                    'onlink': None,
                    'weight': None
                }]
            },
            {
                'prefix': '10.0.1.0/24',
                'primary': '*',
                'proto': 'static4',
                'since': since_field(),
                'type': ['static', 'univ'],
                'weight': '200',
                'nexthops': [{
                    'gateway': '192.168.0.4',
                    'interface': 'eth0',
                    'mpls': None,
                    'onlink': None,
                    'weight': None
                }]
            },
            {
                'prefix': '10.0.2.0/24',
                'primary': '*',
                'proto': 'static4',
                'since': since_field(),
                'type': ['static', 'univ'],
                'weight': '200',
                'nexthops': [{
                    'gateway': '192.168.0.5',
                    'interface': 'eth0',
                    'mpls': None,
                    'onlink': None,
                    'weight': None
                }]
            }
        ]

        assert result == correct_result, 'The show_route_table() result does not match what it should be'

    def test_show_route_table_t_kernel6(self):
        """Test show_route_table."""

        birdclient = BirdClient()
        result = birdclient.show_route_table('t_kernel6', self._load_file('test_show_route_table_t_kernel6.txt'))

        correct_result = [
            {
                'prefix': 'fec0:20::/64',
                'primary': '*',
                'proto': 'static6',
                'since': since_field(),
                'type': ['static', 'univ'],
                'weight': '200',
                'nexthops': [{
                    'gateway': 'fec0::5',
                    'interface': 'eth0',
                    'mpls': None,
                    'onlink': None,
                    'weight': None
                }]
            },
            {
                'prefix': 'fec0:10::/64',
                'primary': '*',
                'proto': 'static6',
                'since': since_field(),
                'type': ['static', 'univ'],
                'weight': '200',
                'nexthops': [{
                    'gateway': 'fec0::4',
                    'interface': 'eth0',
                    'mpls': None,
                    'onlink': None,
                    'weight': None
                }]
            }
        ]

        assert result == correct_result, 'The show_route_table() result does not match what it should be'

    def test_show_route_table_t_ospf4(self):
        """Test show_route_table."""

        birdclient = BirdClient()
        result = birdclient.show_route_table('t_ospf4', self._load_file('test_show_route_table_t_ospf4.txt'))

        correct_result = [
            {
                'prefix': '172.16.100.0/24',
                'primary': None,
                'proto': 'kernel4',
                'since': since_field(),
                'type': ['inherit', 'univ'],
                'weight': '10',
                'nexthops': [{
                    'gateway': '172.16.10.10',
                    'interface': 'eth9',
                    'mpls': None,
                    'onlink': None,
                    'weight': None
                }]
            },
            {
                'prefix': '10.0.1.0/24',
                'primary': '*',
                'proto': 'static4',
                'since': since_field(),
                'type': ['static', 'univ'],
                'weight': '200',
                'nexthops': [{
                    'gateway': '192.168.0.4',
                    'interface': 'eth0',
                    'mpls': None,
                    'onlink': None,
                    'weight': None
                }]
            },
            {
                'prefix': '10.0.2.0/24',
                'primary': '*',
                'proto': 'static4',
                'since': since_field(),
                'type': ['static', 'univ'],
                'weight': '200',
                'nexthops': [{
                    'gateway': '192.168.0.5',
                    'interface': 'eth0',
                    'mpls': None,
                    'onlink': None,
                    'weight': None
                }]
            }
        ]

        assert result == correct_result, 'The show_route_table() result does not match what it should be'

    def test_show_route_table_t_ospf6_1(self):
        """Test show_route_table."""

        birdclient = BirdClient()
        result = birdclient.show_route_table('t_ospf6', self._load_file('test_show_route_table_t_ospf6-1.txt'))

        correct_result = [
            {
                'prefix': 'fec0:20::/64',
                'primary': '*',
                'proto': 'static6',
                'since': since_field(),
                'type': ['static', 'univ'],
                'weight': '200',
                'nexthops': [{
                    'gateway': 'fec0::5',
                    'interface': 'eth0',
                    'mpls': None,
                    'onlink': None,
                    'weight': None
                }]
            },
            {
                'prefix': 'fec0:10::/64',
                'primary': '*',
                'proto': 'static6',
                'since': since_field(),
                'type': ['static', 'univ'],
                'weight': '200',
                'nexthops': [{
                    'gateway': 'fec0::4',
                    'interface': 'eth0',
                    'mpls': None,
                    'onlink': None,
                    'weight': None
                }]
            }
        ]

        assert result == correct_result, 'The show_route_table() result does not match what it should be'

    def test_show_route_table_t_ospf6_2(self):
        """Test show_route_table."""

        birdclient = BirdClient()
        result = birdclient.show_route_table('t_ospf6', self._load_file('test_show_route_table_t_ospf6-2.txt'))

        correct_result = [
            {
                'metric1': '20',
                'metric2': '10000',
                'ospf_type': 'E2',
                'pref': '150',
                'prefix': 'fec0:20::/64',
                'proto': 'ospf6',
                'router_id': '172.16.10.1',
                'since': since_field(),
                'tag': None,
                'type': ['OSPF-E2', 'univ'],
                'nexthops': [{
                    'gateway': 'fe80::8c84:28ff:fe6c:40ae',
                    'interface': 'eth0',
                    'mpls': None,
                    'onlink': None,
                    'weight': None
                }]
            },
            {
                'metric1': '20',
                'metric2': '10000',
                'ospf_type': 'E2',
                'pref': '150',
                'prefix': 'fec0:10::/64',
                'proto': 'ospf6',
                'router_id': '172.16.10.1',
                'since': since_field(),
                'tag': None,
                'type': ['OSPF-E2', 'univ'],
                'nexthops': [{
                    'gateway': 'fe80::8c84:28ff:fe6c:40ae',
                    'interface': 'eth0',
                    'mpls': None,
                    'onlink': None,
                    'weight': None
                }]
            },
            {
                'metric1': '20',
                'metric2': None,
                'ospf_type': 'I',
                'pref': '150',
                'prefix': 'fec0::/64',
                'proto': 'ospf6',
                'router_id': '172.16.10.1',
                'since': since_field(),
                'tag': None,
                'type': ['OSPF', 'univ'],
                'nexthops': [{
                    'gateway': 'fe80::8c84:28ff:fe6c:40ae',
                    'interface': 'eth0',
                    'mpls': None,
                    'onlink': None,
                    'weight': None
                }]
            },
            {
                'metric1': '30',
                'metric2': None,
                'ospf_type': 'I',
                'pref': '150',
                'prefix': 'fefe::/64',
                'proto': 'ospf6',
                'router_id': '172.16.10.1',
                'since': since_field(),
                'tag': None,
                'type': ['OSPF', 'univ'],
                'nexthops': [{
                    'gateway': 'fe80::8c84:28ff:fe6c:40ae',
                    'interface': 'eth0',
                    'mpls': None,
                    'onlink': None,
                    'weight': None
                }]
            },
            {
                'metric1': '10',
                'metric2': None,
                'ospf_type': 'I',
                'pref': '150',
                'prefix': 'fec0:1::/64',
                'proto': 'ospf6',
                'router_id': '0.0.0.3',
                'since': since_field(),
                'tag': None,
                'type': ['OSPF', 'univ'],
                'nexthops': [{
                    'interface': 'eth0',
                    'mpls': None,
                    'onlink': None,
                    'weight': None
                }]
            },
            {
                'metric1': '30',
                'metric2': '10000',
                'ospf_type': 'E2',
                'pref': '150',
                'prefix': 'fefe:1::/64',
                'proto': 'ospf6',
                'router_id': '172.16.10.1',
                'since': since_field(),
                'tag': None,
                'type': ['OSPF-E2', 'univ'],
                'nexthops': [{
                    'gateway': 'fe80::8c84:28ff:fe6c:40ae',
                    'interface': 'eth0',
                    'mpls': None,
                    'onlink': None,
                    'weight': None
                }]
            }
        ]

        assert result == correct_result, 'The show_route_table() result does not match what it should be'

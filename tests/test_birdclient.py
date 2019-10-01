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
            'ospf4': {'info': 'Alone',
                      'name': 'ospf4',
                      'proto': 'OSPF',
                      'since': '2019-09-01 13:13:28',
                      'state': 'up',
                      'table': 't_ospf4'},
            'ospf6': {'info': 'Running',
                      'name': 'ospf6',
                      'proto': 'OSPF',
                      'since': '2019-09-01 13:13:28',
                      'state': 'up',
                      'table': 't_ospf6'},
            'p_ospf4_to_kernel4': {'info': 't_ospf4 <=> t_kernel4',
                                   'name': 'p_ospf4_to_kernel4',
                                   'proto': 'Pipe',
                                   'since': '2019-09-01 13:13:28',
                                   'state': 'up',
                                   'table': '---'},
            'p_ospf4_to_static4': {'info': 't_ospf4 <=> t_static4',
                                   'name': 'p_ospf4_to_static4',
                                   'proto': 'Pipe',
                                   'since': '2019-09-01 13:13:28',
                                   'state': 'up',
                                   'table': '---'},
            'p_ospf6_to_kernel6': {'info': 't_ospf6 <=> t_kernel6',
                                   'name': 'p_ospf6_to_kernel6',
                                   'proto': 'Pipe',
                                   'since': '2019-09-01 13:13:28',
                                   'state': 'up',
                                   'table': '---'},
            'p_ospf6_to_static6': {'info': 't_ospf6 <=> t_static6',
                                   'name': 'p_ospf6_to_static6',
                                   'proto': 'Pipe',
                                   'since': '2019-09-01 13:13:28',
                                   'state': 'up',
                                   'table': '---'},
            'p_static4_to_kernel4': {'info': 't_static4 <=> t_kernel4',
                                     'name': 'p_static4_to_kernel4',
                                     'proto': 'Pipe',
                                     'since': '2019-09-01 13:13:28',
                                     'state': 'up',
                                     'table': '---'},
            'p_static6_to_kernel6': {'info': 't_static6 <=> t_kernel6',
                                     'name': 'p_static6_to_kernel6',
                                     'proto': 'Pipe',
                                     'since': '2019-09-01 13:13:28',
                                     'state': 'up',
                                     'table': '---'}
        }

        assert result == correct_result, 'The show_protocols() result does not match what it should be'

    def test_show_route_table_t_static4(self):
        """Test show_route_table."""

        birdclient = BirdClient()
        result = birdclient.show_route_table('t_static4', self._load_file('test_show_route_table_t_static4.txt'))

        correct_result = {
            '10.0.1.0/24': [{'nexthops': [{'gateway': '192.168.0.4', 'interface': 'eth0'}],
                             'pref': '200',
                             'prefix_type': 'unicast',
                             'protocol': 'static4',
                             'since': '2019-09-01 13:36:14',
                             'type': ['static', 'univ']}],
            '10.0.2.0/24': [{'nexthops': [{'gateway': '192.168.0.5', 'interface': 'eth0'}],
                             'pref': '200',
                             'prefix_type': 'unicast',
                             'protocol': 'static4',
                             'since': '2019-09-01 13:36:14',
                             'type': ['static', 'univ']}]
        }

        assert result == correct_result, 'The show_route_table() result does not match what it should be'

    def test_show_route_table_t_static6(self):
        """Test show_route_table."""

        birdclient = BirdClient()
        result = birdclient.show_route_table('t_static6', self._load_file('test_show_route_table_t_static6.txt'))

        correct_result = {
            'fec0:10::/64': [{'nexthops': [{'gateway': 'fec0::4', 'interface': 'eth0'}],
                              'pref': '200',
                              'prefix_type': 'unicast',
                              'protocol': 'static6',
                              'since': '2019-09-01 13:36:14',
                              'type': ['static', 'univ']}],
            'fec0:20::/64': [{'nexthops': [{'gateway': 'fec0::5', 'interface': 'eth0'}],
                              'pref': '200',
                              'prefix_type': 'unicast',
                              'protocol': 'static6',
                              'since': '2019-09-01 13:36:14',
                              'type': ['static', 'univ']}]
        }

        assert result == correct_result, 'The show_route_table() result does not match what it should be'

    def test_show_route_table_t_kernel4(self):
        """Test show_route_table."""

        birdclient = BirdClient()
        result = birdclient.show_route_table('t_kernel4', self._load_file('test_show_route_table_t_kernel4.txt'))

        correct_result = {
            '10.0.1.0/24': [{'nexthops': [{'gateway': '192.168.0.4', 'interface': 'eth0'}],
                             'pref': '200',
                             'prefix_type': 'unicast',
                             'protocol': 'static4',
                             'since': '2019-09-01 13:36:14',
                             'type': ['static', 'univ']}],
            '10.0.2.0/24': [{'nexthops': [{'gateway': '192.168.0.5', 'interface': 'eth0'}],
                             'pref': '200',
                             'prefix_type': 'unicast',
                             'protocol': 'static4',
                             'since': '2019-09-01 13:36:14',
                             'type': ['static', 'univ']}],
            '172.16.100.0/24': [{'nexthops': [{'gateway': '172.16.10.10',
                                               'interface': 'eth9'}],
                                 'pref': '10',
                                 'prefix_type': 'unicast',
                                 'protocol': 'kernel4',
                                 'since': '2019-09-01 13:36:14',
                                 'type': ['inherit', 'univ']}]
        }

        assert result == correct_result, 'The show_route_table() result does not match what it should be'

    def test_show_route_table_t_kernel6(self):
        """Test show_route_table."""

        birdclient = BirdClient()
        result = birdclient.show_route_table('t_kernel6', self._load_file('test_show_route_table_t_kernel6.txt'))

        correct_result = {
            'fec0:10::/64': [{'nexthops': [{'gateway': 'fec0::4', 'interface': 'eth0'}],
                              'pref': '200',
                              'prefix_type': 'unicast',
                              'protocol': 'static6',
                              'since': '2019-09-01 13:36:14',
                              'type': ['static', 'univ']}],
            'fec0:20::/64': [{'nexthops': [{'gateway': 'fec0::5', 'interface': 'eth0'}],
                              'pref': '200',
                              'prefix_type': 'unicast',
                              'protocol': 'static6',
                              'since': '2019-09-01 13:36:14',
                              'type': ['static', 'univ']}]
        }

        assert result == correct_result, 'The show_route_table() result does not match what it should be'

    def test_show_route_table_t_ospf4(self):
        """Test show_route_table."""

        birdclient = BirdClient()
        result = birdclient.show_route_table('t_ospf4', self._load_file('test_show_route_table_t_ospf4.txt'))

        correct_result = {
            '10.0.1.0/24': [{'nexthops': [{'gateway': '192.168.0.4', 'interface': 'eth0'}],
                             'pref': '200',
                             'prefix_type': 'unicast',
                             'protocol': 'static4',
                             'since': '2019-09-01 13:36:14',
                             'type': ['static', 'univ']}],
            '10.0.2.0/24': [{'nexthops': [{'gateway': '192.168.0.5', 'interface': 'eth0'}],
                             'pref': '200',
                             'prefix_type': 'unicast',
                             'protocol': 'static4',
                             'since': '2019-09-01 13:36:14',
                             'type': ['static', 'univ']}],
            '100.64.43.2/31': [{'attributes': {'OSPF.metric1': '20',
                                               'OSPF.router_id': '100.64.20.1'},
                                'metric1': '20',
                                'nexthops': [{'gateway': '100.64.20.1',
                                              'interface': 'eth0'}],
                                'ospf_type': 'I',
                                'pref': '150',
                                'prefix_type': 'unicast',
                                'protocol': 'ospf4',
                                'router_id': '100.64.20.1',
                                'since': '2019-09-30 17:14:09',
                                'type': ['OSPF', 'univ']}],
            '100.64.50.2/31': [{'attributes': {'OSPF.metric1': '40',
                                               'OSPF.router_id': '100.64.10.2'},
                                'metric1': '40',
                                'nexthops': [{'gateway': '100.64.20.1',
                                              'interface': 'eth0',
                                              'weight': '1'},
                                             {'gateway': '100.64.20.5',
                                              'interface': 'eth0',
                                              'weight': '1'}],
                                'ospf_type': 'I',
                                'pref': '150',
                                'prefix_type': 'unicast',
                                'protocol': 'ospf4',
                                'router_id': '100.64.10.2',
                                'since': '2019-09-30 17:14:13',
                                'type': ['OSPF', 'univ']}],
            '100.90.0.0/28': [{'attributes': {'OSPF.metric1': '40',
                                              'OSPF.metric2': '10000',
                                              'OSPF.router_id': '100.64.10.2',
                                              'OSPF.tag': '0x00000000'},
                               'metric1': '40',
                               'metric2': '10000',
                               'nexthops': [{'gateway': '100.64.20.1',
                                             'interface': 'eth0',
                                             'weight': '1'},
                                            {'gateway': '100.64.20.5',
                                             'interface': 'eth0',
                                             'weight': '1'}],
                               'ospf_type': 'E2',
                               'pref': '150',
                               'prefix_type': 'unicast',
                               'protocol': 'ospf4',
                               'router_id': '100.64.10.2',
                               'since': '2019-09-30 17:14:13',
                               'type': ['OSPF-E2', 'univ']}],
            '172.16.100.0/24': [{'nexthops': [{'gateway': '172.16.10.10',
                                               'interface': 'eth9'}],
                                 'pref': '10',
                                 'prefix_type': 'unicast',
                                 'protocol': 'kernel4',
                                 'since': '2019-09-01 13:36:14',
                                 'type': ['inherit', 'univ']}]
        }

        assert result == correct_result, 'The show_route_table() result does not match what it should be'

    def test_show_route_table_t_ospf6_1(self):
        """Test show_route_table."""

        birdclient = BirdClient()
        result = birdclient.show_route_table('t_ospf6', self._load_file('test_show_route_table_t_ospf6-1.txt'))

        correct_result = {
            'fec0:10::/64': [{'nexthops': [{'gateway': 'fec0::4', 'interface': 'eth0'}],
                              'pref': '200',
                              'prefix_type': 'unicast',
                              'protocol': 'static6',
                              'since': '2019-09-01 13:36:14',
                              'type': ['static', 'univ']}],
            'fec0:20::/64': [{'nexthops': [{'gateway': 'fec0::5', 'interface': 'eth0'}],
                              'pref': '200',
                              'prefix_type': 'unicast',
                              'protocol': 'static6',
                              'since': '2019-09-01 13:36:14',
                              'type': ['static', 'univ']}]
        }

        assert result == correct_result, 'The show_route_table() result does not match what it should be'

    def test_show_route_table_t_ospf6_2(self):
        """Test show_route_table."""

        birdclient = BirdClient()
        result = birdclient.show_route_table('t_ospf6', self._load_file('test_show_route_table_t_ospf6-2.txt'))

        correct_result = {
            'fc00:90::/64': [{'attributes': {'OSPF.metric1': '40',
                                             'OSPF.metric2': '10000',
                                             'OSPF.router_id': '100.64.10.2',
                                             'OSPF.tag': '0x00000000'},
                              'metric1': '40',
                              'metric2': '10000',
                              'nexthops': [{'gateway': 'fe80::20:1ff:fe00:1',
                                            'interface': 'eth0',
                                            'weight': '1'},
                                           {'gateway': 'fe80::20:1ff:fe02:1',
                                            'interface': 'eth0',
                                            'weight': '1'}],
                              'ospf_type': 'E2',
                              'pref': '150',
                              'prefix_type': 'unicast',
                              'protocol': 'ospf6',
                              'router_id': '100.64.10.2',
                              'since': '2019-09-30 17:14:13',
                              'type': ['OSPF-E2', 'univ']}],
            'fc50::2/127': [{'attributes': {'OSPF.metric1': '40',
                                            'OSPF.router_id': '100.64.10.2'},
                             'metric1': '40',
                             'nexthops': [{'gateway': 'fe80::20:1ff:fe00:1',
                                           'interface': 'eth0',
                                           'weight': '1'},
                                          {'gateway': 'fe80::20:1ff:fe02:1',
                                           'interface': 'eth0',
                                           'weight': '1'}],
                             'ospf_type': 'I',
                             'pref': '150',
                             'prefix_type': 'unicast',
                             'protocol': 'ospf6',
                             'router_id': '100.64.10.2',
                             'since': '2019-09-30 17:14:13',
                             'type': ['OSPF', 'univ']}],
            'fec0:20::/64': [{'metric1': '20',
                              'metric2': '10000',
                              'nexthops': [{'gateway': 'fe80::8c84:28ff:fe6c:40ae',
                                            'interface': 'eth0'}],
                              'ospf_type': 'E2',
                              'pref': '150',
                              'prefix_type': 'unicast',
                              'protocol': 'ospf6',
                              'router_id': '172.16.10.1',
                              'since': '2019-09-01 14:20:00',
                              'type': ['OSPF-E2', 'univ']}],
            'fec0::/64': [{'metric1': '20',
                           'nexthops': [{'gateway': 'fe80::8c84:28ff:fe6c:40ae',
                                         'interface': 'eth0'}],
                           'ospf_type': 'I',
                           'pref': '150',
                           'prefix_type': 'unicast',
                           'protocol': 'ospf6',
                           'router_id': '172.16.10.1',
                           'since': '2019-09-01 14:19:58',
                           'type': ['OSPF', 'univ']}]
        }

        assert result == correct_result, 'The show_route_table() result does not match what it should be'

    def test_show_route_table_t_bgp4(self):
        """Test show_route_table."""

        birdclient = BirdClient()
        result = birdclient.show_route_table('t_bgp4', self._load_file('test_show_route_table_t_bgp4.txt'))

        correct_result = {
            '100.100.0.0/24': [{'asn': 'AS65001',
                                'attributes': {'BGP.as_path': '65001',
                                               'BGP.cluster_list': '0.0.0.1',
                                               'BGP.large_community': [('65000',
                                                                        '1',
                                                                        '900'),
                                                                       ('65000', '3', '2'),
                                                                       ('65000',
                                                                        '4',
                                                                        '65004'),
                                                                       ('65001',
                                                                        '3',
                                                                        '1')],
                                               'BGP.local_pref': '750',
                                               'BGP.next_hop': '100.64.50.3',
                                               'BGP.origin': 'IGP',
                                               'BGP.originator_id': '100.64.10.2'},
                                'bestpath': True,
                                'bgp_type': 'i',
                                'from': '100.64.10.3',
                                'nexthops': [{'gateway': '100.64.20.1',
                                              'interface': 'eth0',
                                              'weight': '1'},
                                             {'gateway': '100.64.20.5',
                                              'interface': 'eth0',
                                              'weight': '1'}],
                                'pref': '100',
                                'prefix_type': 'unicast',
                                'protocol': 'bgp_AS65000_rr1_peer4',
                                'since': '2019-09-30 17:14:14',
                                'type': ['BGP', 'univ']}],
            '100.201.0.0/24': [{'asn': 'AS65006',
                                'attributes': {'BGP.as_path': '65006',
                                               'BGP.cluster_list': '0.0.0.1',
                                               'BGP.large_community': [('65000', '3', '3'),
                                                                       ('65006',
                                                                        '3',
                                                                        '1')],
                                               'BGP.local_pref': '450',
                                               'BGP.next_hop': '100.64.40.11',
                                               'BGP.origin': 'IGP',
                                               'BGP.originator_id': '100.64.10.1'},
                                'bestpath': True,
                                'bgp_type': 'i',
                                'from': '100.64.10.3',
                                'nexthops': [{'gateway': '100.64.20.1',
                                              'interface': 'eth0',
                                              'weight': '1'},
                                             {'gateway': '100.64.20.5',
                                              'interface': 'eth0',
                                              'weight': '1'}],
                                'pref': '100',
                                'prefix_type': 'unicast',
                                'protocol': 'bgp_AS65000_rr1_peer4',
                                'since': '2019-09-30 17:14:14',
                                'type': ['BGP', 'univ']},
                               {'asn': 'AS65004',
                                'attributes': {'BGP.as_path': '65004',
                                               'BGP.cluster_list': '0.0.0.1',
                                               'BGP.large_community': [('65000', '3', '4'),
                                                                       ('65004',
                                                                        '3',
                                                                        '1')],
                                               'BGP.local_pref': '150',
                                               'BGP.next_hop': '100.64.43.2',
                                               'BGP.origin': 'IGP',
                                               'BGP.originator_id': '100.64.20.1'},
                                'bestpath': False,
                                'bgp_type': 'i',
                                'from': '100.64.20.3',
                                'nexthops': [{'gateway': '100.64.20.1',
                                              'interface': 'eth0'}],
                                'pref': '100',
                                'prefix_type': 'unicast',
                                'protocol': 'bgp_AS65000_rr2_peer4',
                                'since': '2019-09-30 17:14:09',
                                'type': ['BGP', 'univ']}]
        }

        assert result == correct_result, 'The show_route_table() result does not match what it should be'

    def test_show_route_table_t_bgp6(self):
        """Test show_route_table."""

        birdclient = BirdClient()
        result = birdclient.show_route_table('t_bgp6', self._load_file('test_show_route_table_t_bgp6.txt'))

        correct_result = {
            'fc00:130::/48': [{'asn': 'AS65007',
                               'attributes': {'BGP.as_path': '65007',
                                              'BGP.large_community': [('65000',
                                                                       '4',
                                                                       '65414'),
                                                                      ('65007', '3', '1'),
                                                                      ('65000', '3', '2'),
                                                                      ('65000',
                                                                       '1',
                                                                       '901')],
                                              'BGP.local_pref': '750',
                                              'BGP.next_hop': 'fc61::3 '
                                                              'fe80::61:1ff:fe00:1',
                                              'BGP.origin': 'IGP'},
                               'bestpath': True,
                               'bgp_type': 'i',
                               'nexthops': [{'gateway': 'fc61::3', 'interface': 'eth1'}],
                               'pref': '100',
                               'prefix_type': 'unicast',
                               'protocol': 'bgp_AS65007_client3_peer6',
                               'since': '2019-09-30 17:14:00',
                               'type': ['BGP', 'univ']},
                              {'attributes': {'BGP.as_path': '',
                                              'BGP.cluster_list': '0.0.0.1',
                                              'BGP.large_community': [('65000', '3', '1')],
                                              'BGP.local_pref': '940',
                                              'BGP.next_hop': 'fc50::5',
                                              'BGP.origin': 'IGP',
                                              'BGP.originator_id': '100.64.10.2'},
                               'bestpath': False,
                               'bgp_type': 'i',
                               'from': 'fc20::3',
                               'nexthops': [{'gateway': 'fe80::20:1ff:fe00:1',
                                             'interface': 'eth0',
                                             'weight': '1'},
                                            {'gateway': 'fe80::20:1ff:fe02:1',
                                             'interface': 'eth0',
                                             'weight': '1'}],
                               'pref': '100',
                               'prefix_type': 'unicast',
                               'protocol': 'bgp_AS65000_rr2_peer6',
                               'since': '2019-09-30 17:14:20',
                               'type': ['BGP', 'univ']}],
            'fc20::/64': [{'attributes': {'BGP.as_path': '',
                                          'BGP.cluster_list': '0.0.0.1',
                                          'BGP.large_community': [('65000', '3', '1')],
                                          'BGP.local_pref': '930',
                                          'BGP.next_hop': 'fc20::1',
                                          'BGP.origin': 'IGP',
                                          'BGP.originator_id': '100.64.20.1'},
                           'bestpath': True,
                           'bgp_type': 'i',
                           'from': 'fc10::3',
                           'nexthops': [{'gateway': 'fc20::1', 'interface': 'eth0'}],
                           'pref': '100',
                           'prefix_type': 'unicast',
                           'protocol': 'bgp_AS65000_rr1_peer6',
                           'since': '2019-09-30 17:14:15',
                           'type': ['BGP', 'univ']},
                          {'asn': 'AS65006',
                           'attributes': {'BGP.as_path': '65006',
                                          'BGP.cluster_list': '0.0.0.1',
                                          'BGP.large_community': [('65000', '3', '3'),
                                                                  ('65006', '3', '1')],
                                          'BGP.local_pref': '450',
                                          'BGP.next_hop': 'fc40::11 fe80::40:1ff:fe00:1',
                                          'BGP.origin': 'IGP',
                                          'BGP.originator_id': '100.64.10.1'},
                           'bestpath': False,
                           'bgp_type': 'i',
                           'from': 'fc20::3',
                           'nexthops': [{'gateway': 'fe80::20:1ff:fe00:1',
                                         'interface': 'eth0',
                                         'weight': '1'},
                                        {'gateway': 'fe80::20:1ff:fe02:1',
                                         'interface': 'eth0',
                                         'weight': '1'}],
                           'pref': '100',
                           'prefix_type': 'unicast',
                           'protocol': 'bgp_AS65000_rr2_peer6',
                           'since': '2019-09-30 17:14:14',
                           'type': ['BGP', 'univ']}]
        }

        assert result == correct_result, 'The show_route_table() result does not match what it should be'

    def test_show_route_table_t_rip4(self):
        """Test show_route_table."""

        birdclient = BirdClient()
        result = birdclient.show_route_table('t_rip4', self._load_file('test_show_route_table_t_rip4.txt'))

        correct_result = {
            '192.168.10.0/24': [{'metric1': '3',
                                 'nexthops': [{'gateway': '192.168.0.1',
                                               'interface': 'eth0'}],
                                 'pref': '120',
                                 'prefix_type': 'unicast',
                                 'protocol': 'rip4',
                                 'since': '2019-10-01 17:59:41'}],
            '192.168.21.0/24': [{'nexthops': [{'gateway': '192.168.20.3',
                                               'interface': 'eth1'}],
                                 'pref': '200',
                                 'prefix_type': 'unicast',
                                 'protocol': 'static4',
                                 'since': '2019-10-01 17:59:38'}]
        }

        assert result == correct_result, 'The show_route_table() result does not match what it should be'

    def test_show_route_table_t_rip6(self):
        """Test show_route_table."""

        birdclient = BirdClient()
        result = birdclient.show_route_table('t_rip6', self._load_file('test_show_route_table_t_rip6.txt'))

        correct_result = {
            'fc10::/64': [{'metric1': '3',
                           'nexthops': [{'gateway': 'fe80::1:ff:fe00:1',
                                         'interface': 'eth0'}],
                           'pref': '120',
                           'prefix_type': 'unicast',
                           'protocol': 'rip6',
                           'since': '2019-10-01 17:59:42'}],
            'fc21::/64': [{'nexthops': [{'gateway': 'fc20::3', 'interface': 'eth1'}],
                           'pref': '200',
                           'prefix_type': 'unicast',
                           'protocol': 'static6',
                           'since': '2019-10-01 17:59:38'}]
        }

        assert result == correct_result, 'The show_route_table() result does not match what it should be'

    def test_show_route_table_t_direct4(self):
        """Test show_route_table."""

        birdclient = BirdClient()
        result = birdclient.show_route_table('t_direct4', self._load_file('test_show_route_table_t_direct4.txt'))

        correct_result = {
            '192.168.10.0/24': [{'nexthops': [{'interface': 'eth1'}],
                                 'pref': '240',
                                 'prefix_type': 'unicast',
                                 'protocol': 'direct4_rip',
                                 'since': '2019-10-01 18:42:53'}]
        }

        assert result == correct_result, 'The show_route_table() result does not match what it should be'

    def test_show_route_table_t_direct6(self):
        """Test show_route_table."""

        birdclient = BirdClient()
        result = birdclient.show_route_table('t_direct6', self._load_file('test_show_route_table_t_direct6.txt'))

        correct_result = {
            'fc10::/64': [{'nexthops': [{'interface': 'eth1'}],
                           'pref': '240',
                           'prefix_type': 'unicast',
                           'protocol': 'direct6_rip',
                           'since': '2019-10-01 18:42:53'}]
        }

        assert result == correct_result, 'The show_route_table() result does not match what it should be'

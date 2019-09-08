# Copyright (C) 2019, AllWorldIT.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""BIRD client class."""

import re
import socket

from typing import Any, Dict, List, Optional


class Birdc:
    """BIRD client class."""

    # Socket file
    _socket_file: str
    # Ending lines for bird control channel
    _ending_lines: List[bytes]

    def __init__(self, socket_file: str):
        """Initialize the object."""

        # Set socket file
        self._socket_file = socket_file
        # Setup ending lines
        self._ending_lines = (b'0000 ', b'0013 ', b'8001 ', b'8003 ', b'9001 ')

    def show_status(self, data: Optional[List[str]] = None) -> Dict[str, str]:
        """Return parsed BIRD status."""
        # 0001 BIRD 2.0.4 ready.
        # 1000-BIRD 2.0.4
        # 1011-Router ID is 172.16.10.1
        #  Current server time is 2019-08-15 12:42:51.638
        #  Last reboot on 2019-08-15 12:42:47.592
        #  Last reconfiguration on 2019-08-15 12:42:47.592
        # 0013 Daemon is up and running

        # Grab status
        if not data:
            data = self.query('show status')

        # Return structure
        res = {
            'version': '',
            'router_id': '',
            'server_time': '',
            'last_reboot': '',
            'last_reconfiguration': '',
        }

        # Loop with data to grab information we need
        for line in data:
            # Grab BIRD version
            match = re.match(r'^0001 BIRD (?P<version>[0-9\.]+) ready\.$', line)
            if match:
                res['version'] = match.group('version')
            # Grab Router ID
            match = re.match(r'^1011-Router ID is (?P<router_id>[0-9\.]+)$', line)
            if match:
                res['router_id'] = match.group('router_id')
            # Current server time
            match = re.match(r'^ Current server time is (?P<server_time>[0-9\.\s:\-]+)$', line)
            if match:
                res['server_time'] = match.group('server_time')
            # Last reboot
            match = re.match(r'^ Last reboot on (?P<last_reboot>[0-9\.\s:\-]+)$', line)
            if match:
                res['last_reboot'] = match.group('last_reboot')
            # Last reconfiguration
            match = re.match(r'^ Last reconfiguration on (?P<last_reconfig>[0-9\.\s:\-]+)$', line)
            if match:
                res['last_reconfiguration'] = match.group('last_reconfig')

        return res

    def show_protocols(self, data: Optional[List[str]] = None) -> Dict[str, Any]:
        """Return parsed BIRD protocols."""
        # 0001 BIRD 2.0.4 ready.
        # 2002-Name       Proto      Table      State  Since         Info
        # 1002-device1    Device     ---        up     13:13:28.641
        #  kernel4    Kernel     t_kernel4  up     13:13:28.641
        #  kernel6    Kernel     t_kernel6  up     13:13:28.641
        #  static4    Static     t_static4  up     13:13:28.641
        #  static6    Static     t_static6  up     13:13:28.641
        #  p_static4_to_kernel4 Pipe       ---        up     13:13:28.641  t_static4 <=> t_kernel4
        #  p_static6_to_kernel6 Pipe       ---        up     13:13:28.641  t_static6 <=> t_kernel6
        #  ospf4      OSPF       t_ospf4    up     13:13:28.641  Alone
        #  ospf6      OSPF       t_ospf6    up     13:13:28.641  Running
        #  p_ospf4_to_kernel4 Pipe       ---        up     13:13:28.641  t_ospf4 <=> t_kernel4
        #  p_ospf6_to_kernel6 Pipe       ---        up     13:13:28.641  t_ospf6 <=> t_kernel6
        #  p_ospf4_to_static4 Pipe       ---        up     13:13:28.641  t_ospf4 <=> t_static4
        #  p_ospf6_to_static6 Pipe       ---        up     13:13:28.641  t_ospf6 <=> t_static6
        # 0000

        # Grab protocols
        if not data:
            data = self.query('show protocols')

        res = {}

        # Loop with data to grab information we need
        for line in data:
            # Grab BIRD version
            match = re.match(r'^(?:1002-| )'
                             r'(?P<name>\S+)\s+'
                             r'(?P<proto>\S+)\s+'
                             r'(?P<table>\S+)\s+'
                             r'(?P<state>\S+)\s+'
                             r'(?P<since>\S+)\s+'
                             r'(?P<info>.*)', line)
            if match:
                # Build up the protocol
                protocol = {}
                protocol['name'] = match.group('name')
                protocol['proto'] = match.group('proto')
                protocol['table'] = match.group('table')
                protocol['state'] = match.group('state')
                protocol['since'] = match.group('since')
                protocol['info'] = match.group('info')
                # Save protocol
                res[protocol['name']] = protocol

        return res

    # pylama: ignore=R0915,C901
    def show_route_table(self, table: str, data: Optional[List[str]] = None) -> List:
        """Return parsed BIRD routing table."""
        # 0001 BIRD 2.0.4 ready.
        # 1007-Table t_static4:
        #  10.0.1.0/24          unicast [static4 13:36:14.198] * (200)
        #         via 192.168.0.4 on eth0
        # 1008-   Type: static univ
        # 1007-10.0.2.0/24          unicast [static4 13:36:14.198] * (200)
        #         via 192.168.0.5 on eth0
        # 1008-   Type: static univ
        # 0000

        # 0001 BIRD 2.0.4 ready.
        # 1007-Table t_kernel4:
        #  172.16.100.0/24      unicast [kernel4 13:36:14.199] (10)
        #         via 172.16.10.10 on eth9
        # 1008-   Type: inherit univ
        # 1007-10.0.1.0/24          unicast [static4 13:36:14.199] * (200)
        #         via 192.168.0.4 on eth0
        # 1008-   Type: static univ
        # 1007-10.0.2.0/24          unicast [static4 13:36:14.199] * (200)
        #         via 192.168.0.5 on eth0
        # 1008-   Type: static univ
        # 0000

        # 0001 BIRD 2.0.4 ready.
        # 1007-Table t_ospf4:
        #  172.16.100.0/24      unicast [kernel4 13:36:14.199] (10)
        #         via 172.16.10.10 on eth9
        # 1008-   Type: inherit univ
        # 1007-10.0.1.0/24          unicast [static4 13:36:14.199] * (200)
        #         via 192.168.0.4 on eth0
        # 1008-   Type: static univ
        # 1007-10.0.2.0/24          unicast [static4 13:36:14.199] * (200)
        #         via 192.168.0.5 on eth0
        # 1008-   Type: static univ
        # 0000

        # 0001 BIRD 2.0.4 ready.
        # 1007-Table t_static6:
        #  fec0:20::/64         unicast [static6 13:36:14.708] * (200)
        #         via fec0::5 on eth0
        # 1008-   Type: static univ
        # 1007-fec0:10::/64         unicast [static6 13:36:14.708] * (200)
        #         via fec0::4 on eth0
        # 1008-   Type: static univ
        # 0000

        # 0001 BIRD 2.0.4 ready.
        # 1007-Table t_kernel6:
        #  fec0:20::/64         unicast [static6 13:36:14.708] * (200)
        #         via fec0::5 on eth0
        # 1008-   Type: static univ
        # 1007-fec0:10::/64         unicast [static6 13:36:14.708] * (200)
        #         via fec0::4 on eth0
        # 1008-   Type: static univ
        # 0000

        # 0001 BIRD 2.0.4 ready.
        # 1007-Table t_ospf6:
        #  fec0:20::/64         unicast [static6 13:36:14.708] * (200)
        #         via fec0::5 on eth0
        # 1008-   Type: static univ
        # 1007-fec0:10::/64         unicast [static6 13:36:14.708] * (200)
        #         via fec0::4 on eth0
        # 1008-   Type: static univ
        # 0000

        # 0001 BIRD 2.0.4 ready.
        # 1007-Table t_ospf6:
        #  fec0:20::/64         unicast [ospf6 14:20:00.666] E2 (150/20/10000) [172.16.10.1]
        #         via fe80::8c84:28ff:fe6c:40ae on eth0
        # 1008-   Type: OSPF-E2 univ
        # 1007-fec0:10::/64         unicast [ospf6 14:20:00.666] E2 (150/20/10000) [172.16.10.1]
        #         via fe80::8c84:28ff:fe6c:40ae on eth0
        # 1008-   Type: OSPF-E2 univ
        # 1007-fec0::/64            unicast [ospf6 14:19:58.660] I (150/20) [172.16.10.1]
        #         via fe80::8c84:28ff:fe6c:40ae on eth0
        # 1008-   Type: OSPF univ
        # 1007-fefe::/64            unicast [ospf6 14:20:00.666] I (150/30) [172.16.10.1]
        #         via fe80::8c84:28ff:fe6c:40ae on eth0
        # 1008-   Type: OSPF univ
        # 1007-fec0:1::/64          unicast [ospf6 14:19:58.660] I (150/10) [0.0.0.3]
        #         dev eth0
        # 1008-   Type: OSPF univ
        # 1007-fefe:1::/64          unicast [ospf6 14:20:00.666] E2 (150/30/10000) [172.16.10.1]
        #         via fe80::8c84:28ff:fe6c:40ae on eth0
        # 1008-   Type: OSPF-E2 univ

        # Grab routes
        if not data:
            data = self.query(f'show route table {table} all')

        res = []

        # Loop with data to grab information we need
        route: Dict[str, Any] = {}
        for line in data:
            # Grab a OSPF route
            match = re.match(r'^(?:1007-| )'
                             r'(?P<prefix>\S+)\s+'
                             r'(?P<type>\S+)\s+'
                             r'\[(?P<proto>\S+)\s+'
                             r'(?P<since>\S+)\]\s+'
                             r'(?P<ospf_type>(?:I|IA|E1|E2))?\s*'
                             r'\((?P<pref>\d+)/(?P<metric1>\d+)(?:/(?P<metric2>\d+))?\)'
                             r'(?:\s+\[(?P<tag>[0-9a-f]+)\])?'
                             r'(?:\s+\[(?P<router_id>[0-9\.]+)\])?', line)
            if match:
                # Build the route
                route = {}
                route['prefix'] = match.group('prefix')
                route['type'] = match.group('type')
                route['proto'] = match.group('proto')
                route['since'] = match.group('since')
                route['ospf_type'] = match.group('ospf_type')
                route['pref'] = match.group('pref')
                route['metric1'] = match.group('metric1')
                route['metric2'] = match.group('metric2')
                route['tag'] = match.group('tag')
                route['router_id'] = match.group('router_id')
                # Append route to our results
                res.append(route)
                continue

            # Grab a normal route
            match = re.match(r'^(?:1007-| )'
                             r'(?P<prefix>\S+)\s+'
                             r'(?P<type>\S+)\s+'
                             r'\[(?P<proto>\S+)\s+'
                             r'(?P<since>\S+)\]\s+'
                             r'(?P<primary>\*)?\s*'
                             r'\((?P<weight>\S+)\)', line)
            if match:
                # Build the route
                route = {}
                route['prefix'] = match.group('prefix')
                route['type'] = match.group('type')
                route['proto'] = match.group('proto')
                route['since'] = match.group('since')
                route['primary'] = match.group('primary')
                route['weight'] = match.group('weight')
                # Append the route to our results
                res.append(route)
                continue

            # Grab nexthop details via a gateway
            match = re.match(r'\s+via\s+'
                             r'(?P<gateway>\S+)\s+'
                             r'on (?P<interface>\S+)'
                             r'(?: mpls (?P<mpls>[0-9/]+))?'
                             r'(?: (?P<onlink>onlink))?'
                             r'(?: weight (?P<weight>[0-9]+))?', line)
            if match:
                # Build the nexthop
                if 'nexthops' not in route:
                    route['nexthops'] = []
                nexthop = {}
                nexthop['gateway'] = match.group('gateway')
                nexthop['interface'] = match.group('interface')
                nexthop['mpls'] = match.group('mpls')
                nexthop['onlink'] = match.group('onlink')
                nexthop['weight'] = match.group('weight')
                # Save gateway
                route['nexthops'].append(nexthop)
                continue

            # Grab nexthop details via a device
            match = re.match(r'\s+dev (?P<interface>\S+)'
                             r'(?: mpls (?P<mpls>[0-9/]+))?'
                             r'(?: (?P<onlink>onlink))?'
                             r'(?: weight (?P<weight>[0-9]+))?', line)
            if match:
                # Build the nexthop
                if 'nexthops' not in route:
                    route['nexthops'] = []
                nexthop = {}
                nexthop['interface'] = match.group('interface')
                nexthop['mpls'] = match.group('mpls')
                nexthop['onlink'] = match.group('onlink')
                nexthop['weight'] = match.group('weight')
                # Save gateway
                route['nexthops'].append(nexthop)
                continue

            # Grab type details
            match = re.match(r'1008-\s+'
                             r'Type: (?P<type>.*)', line)
            if match:
                # Work out the types
                if 'type' not in route:
                    route['type'] = []
                route_types = match.group('type').split()
                # Save type
                route['type'] = route_types
                continue

        return res

    def query(self, query: str) -> List[str]:
        """Open a socket to the BIRD daemon, send the query and get the response."""

        # Create a unix socket
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        # Connect to the BIRD daemon
        sock.connect(self._socket_file)

        # Send the query
        sock.send(f'{query}\n'.encode('ascii'))

        # Initialize byte array to store what we get back
        data = bytearray()

        # Loop while we're not done
        done = False
        while not done:
            chunk = sock.recv(10)
            data.extend(chunk)
            # If the last bit of data ends us off in a newline, this may be the end of the stream
            if data.endswith(b'\n'):
                # Check by splitting the lines off
                lines = data.splitlines()
                # Grab last line
                last_line = lines[-1]
                # Check if this is an ending line
                for ending in self._ending_lines:
                    # If it is, then we're done
                    if last_line.startswith(ending):
                        done = True
        # Close socket
        sock.close()

        # Convert data bytes to a string and split into lines
        return data.decode('ascii').splitlines()

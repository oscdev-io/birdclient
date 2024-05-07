#
# SPDX-License-Identifier: MIT
#
# Copyright (C) 2019-2024, AllWorldIT.
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

import os
import re
import socket
from typing import Any, Dict, List, Optional, Union

from .exceptions import BirdClientError, BirdClientNotFoundError, BirdClientParseError
from .version import __version__

__all__ = ["__version__", "BirdClient", "BirdClientError", "BirdClientParseError", "BirdClientNotFoundError"]


# Regex matches
_SINCE_MATCH = r"(?P<since>(?:[0-9]{4}-[0-9]{2}-[0-9]{2} )?[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]{1,3})?)"


class BirdClient:
    """BIRD client class."""

    # Debug flag
    _debug: bool
    # Socket file
    _control_socket: Optional[str]
    # Ending lines for bird control channel
    _ending_lines: List[bytes]

    def __init__(self, control_socket: Optional[str] = None, debug: bool = False):
        """Initialize the object."""

        # Set debug flag
        self._debug = debug

        # Work out which bird socket file to use
        self._control_socket = control_socket
        if not self._control_socket:  # pragma: no cover
            for bird_socket_file in ["/run/bird.ctl", "/run/bird/bird.ctl"]:
                if os.path.exists(bird_socket_file):
                    self._control_socket = bird_socket_file
                    break

        # Setup ending lines
        self._ending_lines = [
            b"0000 ",
            b"0002 ",
            b"0003 ",
            b"0004 ",
            b"0005 ",
            b"0006 ",
            b"0007 ",
            b"0008 ",
            b"0009 ",
            b"0010 ",
            b"0011 ",
            b"0012 ",
            b"0013 ",
            b"0014 ",
            b"0015 ",
            b"0016 ",
            b"0017 ",
            b"0018 ",
            b"0019 ",
            b"0020 ",
            b"0021 ",
            b"0022 ",
            b"0023 ",
            b"0024 ",
            b"0025 ",
            b"8001 ",
            b"8003 ",
            b"9001 ",
        ]

    def show_status(self, data: Optional[List[str]] = None) -> Dict[str, str]:
        """Return parsed BIRD status."""

        # Grab status
        if not data:  # pragma: no cover
            data = self.query(["show", "status"])

        # Return structure
        res = {
            "version": "",
            "router_id": "",
            "server_time": "",
            "last_reboot": "",
            "last_reconfiguration": "",
        }

        # Loop with data to grab information we need
        for line in data:
            # Grab BIRD version
            match = re.match(r"^0001 BIRD (?P<version>[0-9\.]+) ready\.$", line)
            if match:
                res["version"] = match.group("version")
            # Grab Router ID
            match = re.match(r"^1011-Router ID is (?P<router_id>[0-9\.]+)$", line)
            if match:
                res["router_id"] = match.group("router_id")
            # Current server time
            match = re.match(r"^ Current server time is (?P<server_time>[0-9\.\s:\-]+)$", line)
            if match:
                res["server_time"] = match.group("server_time")
            # Last reboot
            match = re.match(r"^ Last reboot on (?P<last_reboot>[0-9\.\s:\-]+)$", line)
            if match:
                res["last_reboot"] = match.group("last_reboot")
            # Last reconfiguration
            match = re.match(r"^ Last reconfiguration on (?P<last_reconfig>[0-9\.\s:\-]+)$", line)
            if match:
                res["last_reconfiguration"] = match.group("last_reconfig")

        return res

    def show_protocol(self, protocol: str, data: Optional[List[str]] = None) -> Dict[str, Any]:  # pylint: disable=too-many-branches
        """Return parsed BIRD protocol."""

        res = self.show_protocols(args=[protocol], data=data)
        if protocol not in res:
            raise BirdClientNotFoundError(f"Protocol '{protocol}' not found")

        return res[protocol]

    def show_protocols(  # noqa: CFQ001 # pylint: disable=R0912,R0915
        self, args: Optional[List[str]] = None, data: Optional[List[str]] = None
    ) -> Dict[str, Dict[str, Any]]:
        """Return parsed BIRD protocol."""

        # Grab protocols
        if not data:  # pragma: no cover
            # Build query
            query = ["show", "protocols", "all"]
            if args:
                query.extend(args)
            # Send query to BIRD
            data = self.query(query)

        res: Dict[str, Any] = {}

        # Loop with data to grab information we need
        protocol: Dict[str, Any] = {}
        for line in data:
            # Grab summary
            match = re.match(
                r"^(?:1002-| )"
                r"(?P<name>\S+)\s+"
                r"(?P<proto>\S+)\s+"
                r"(?P<table>\S+)\s+"
                r"(?P<state>\S+)\s+" + _SINCE_MATCH + r"\s+"
                r"(?P<info>\S+)?\s*"
                r"(?P<info_extra>.*)?",
                line,
            )
            if match:
                table = match.group("table")
                state = match.group("state").lower()
                info = match.group("info")
                # If we have info, lowercase it
                if info:
                    info = info.lower()
                info_extra = match.group("info_extra")
                # If the protocol is BGP and the state is "start", then the state is actually down
                if match.group("proto") == "BGP":
                    # Slighly modify our state
                    if state == "start":
                        state = "down"
                    # And add the extra info separately if this is a BGP protocol
                    info_extra = info_extra.lower()

                    # Change info when it is "active" to "connect" as it swaps between the two
                    if info in ("active", "connect"):
                        info = "connecting"
                    # Next change "passive" to "wait"
                    elif info == "passive":
                        info = "waiting"
                # Check if this is OSPF
                elif match.group("proto") == "OSPF":
                    # If info shows alone it means the state is actually down
                    if info == "alone":
                        state = "down"
                # Else add the extra info onto info for all other protocols
                else:
                    # If we have extra info then add it onto info and blank it
                    if info_extra:
                        info += f" {info_extra}"
                        info_extra = ""

                protocol_name = match.group("name")

                # Build up the protocol
                protocol = {
                    "name": protocol_name,
                    "proto": match.group("proto"),
                    "state": state,
                    "since": match.group("since"),
                    "info": info,
                }
                if table != "---":
                    protocol["table"] = table
                if info_extra:
                    protocol["info_extra"] = info_extra
                # Save protocol
                res[protocol["name"]] = protocol

            # Grab BGP state
            match = re.match(
                r"\s+BGP state:\s+(?P<bgp_state>\S+)",
                line,
            )
            if match:
                protocol["info"] = match.group("bgp_state").lower()
                continue

            # Grab neighbor address
            match = re.match(
                r"\s+Neighbor address:\s+(?P<neighbor_address>\S+)",
                line,
            )
            if match:
                protocol["neighbor_address"] = match.group("neighbor_address")
                continue

            # Grab neighbor AS
            match = re.match(
                r"\s+Neighbor AS:\s+(?P<neighbor_as>\S+)",
                line,
            )
            if match:
                protocol["neighbor_as"] = int(match.group("neighbor_as"))
                continue

            # Grab local AS
            match = re.match(
                r"\s+Local AS:\s+(?P<local_as>\S+)",
                line,
            )
            if match:
                protocol["local_as"] = int(match.group("local_as"))
                continue

            # Grab last error
            match = re.match(
                r"\s+Last error:\s+(?P<last_error>.*)",
                line,
            )
            if match:
                protocol["last_error"] = match.group("last_error").rstrip().lower()
                continue

            # Grab neighbor ID
            match = re.match(
                r"\s+Neighbor ID:\s+(?P<neighbor_id>\S+)",
                line,
            )
            if match:
                protocol["neighbor_id"] = match.group("neighbor_id")
                continue

            # Grab source address
            match = re.match(
                r"\s+Source address:\s+(?P<source_address>\S+)",
                line,
            )
            if match:
                protocol["source_address"] = match.group("source_address")
                continue

            # Grab channel
            match = re.match(
                r"\s+Channel (?P<channel>\S+)",
                line,
            )
            if match:
                protocol["channel"] = match.group("channel").lower()
                continue

            # Grab state
            match = re.match(
                r"\s+State:\s+(?P<state>\S+)",
                line,
            )
            if match:
                protocol["state"] = match.group("state").lower()
                continue

            # Grab table
            match = re.match(
                r"\s+Table:\s+(?P<table>\S+)",
                line,
            )
            if match:
                protocol["table"] = match.group("table")
                continue

            # Grab preference
            match = re.match(
                r"\s+Preference:\s+(?P<preference>\S+)",
                line,
            )
            if match:
                protocol["preference"] = int(match.group("preference"))
                continue

            # Grab input filter
            match = re.match(
                r"\s+Input filter:\s+(?P<input_filter>\S+)",
                line,
            )
            if match:
                protocol["input_filter"] = match.group("input_filter")
                continue

            # Grab output filter
            match = re.match(
                r"\s+Output filter:\s+(?P<output_filter>\S+)",
                line,
            )
            if match:
                protocol["output_filter"] = match.group("output_filter")
                continue

            # Grab import limit
            match = re.match(
                r"\s+Import limit:\s+(?P<import_limit>\S+)",
                line,
            )
            if match:
                protocol["import_limit"] = int(match.group("import_limit"))
                continue

            # Grab import limit action
            match = re.match(
                r"\s+Action:\s+(?P<import_limit_action>\S+)",
                line,
            )
            if match:
                protocol["import_limit_action"] = match.group("import_limit_action")
                continue

            # Grab route count
            match = re.match(
                r"\s+Routes:\s+"
                r"(?P<routes_imported>\d+) imported, "
                r"(?P<routes_exported>\d+) exported, "
                r"(?P<routes_preferred>\d+) preferred",
                line,
            )
            if match:
                protocol["routes_imported"] = int(match.group("routes_imported"))
                protocol["routes_exported"] = int(match.group("routes_exported"))
                continue

            # Grab BGP next hop
            match = re.match(
                r"\s+BGP Next hop:\s+(?P<bgp_next_hop>\S+)",
                line,
            )
            if match:
                protocol["bgp_nexthop"] = match.group("bgp_next_hop")
                continue

            # Grab IGP table
            match = re.match(
                r"\s+IGP IPv[46] table:\s+(?P<igp_table>\S+)",
                line,
            )
            if match:
                protocol["igp_table"] = match.group("igp_table")
                continue

        return res

    def show_route_table(self, table: str, data: Optional[List[str]] = None) -> Dict[Any, Any]:  # pylint: disable=R0914,R0912,R0915
        """Return parsed BIRD routing table."""

        # Grab routes
        return self.show_route(args=["table", table, "all"], data=data)

    def show_route(  # noqa: CFQ001  # pylint: disable=R0914,R0912,R0915
        self, args: Optional[List[str]] = None, data: Optional[List[str]] = None
    ) -> Dict[Any, Any]:
        """Return parsed BIRD routes."""

        # Grab routes
        if not data:  # pragma: no cover
            query = ["show", "route"]
            if args:
                query.extend(args)
            data = self.query(query)

        res: Dict[str, Any] = {}

        # Loop with data to grab information we need
        code = ""
        sources: List[Dict[str, Any]] = []
        source: Dict[str, Any] = {}
        prefix: str = ""
        attrib: str = ""
        value: Any
        for line in data:
            match = re.match(r"^(?P<code>[0-9]{4})-?\s*(?P<line>.*)$", line)
            if match:
                code = match.group("code")
                line = match.group("line")

            # End of output
            if code == "0000":
                # If we had sources, save them
                if sources:
                    res[prefix] = sources
                break

            # Start of output
            if code == "0001":
                continue

            # Route info
            if code == "1007":
                # Exclude the table line
                match = re.match(r"^Table ", line)
                if match:
                    # If we had sources, save them
                    if sources:
                        res[prefix] = sources
                    sources = []
                    source = {}
                    continue

                #
                # Match IPv4 ROA prefix
                #
                match = re.match(
                    r"^\s*(?P<prefix>[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\/[0-9]{1,2})(?P<line>-.+)$",
                    line,
                )
                if match:
                    # If we had sources from a previous route, save them
                    if sources:
                        res[prefix] = sources
                    sources = []
                    source = {}
                    prefix = match.group("prefix")
                    line = match.group("line")

                #
                # Match IPv6 ROA prefix
                #
                match = re.match(
                    r"^\s*(?P<prefix>[a-f0-9:]+\/[0-9]{1,3})(?P<line>-.+)$",
                    line,
                )
                if match:
                    # If we had sources from a previous route, save them
                    if sources:
                        res[prefix] = sources
                    sources = []
                    source = {}
                    prefix = match.group("prefix")
                    line = match.group("line")

                #
                # Match IPv4 prefix
                #
                match = re.match(
                    r"^\s*(?P<prefix>[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\/[0-9]{1,2})\s+(?P<line>.+)$",
                    line,
                )
                if match:
                    # If we had sources from a previous route, save them
                    if sources:
                        res[prefix] = sources
                    sources = []
                    source = {}
                    prefix = match.group("prefix")
                    line = match.group("line")

                #
                # Match IPv6 prefix
                #
                match = re.match(r"^\s*(?P<prefix>[a-f0-9:]+\/[0-9]{1,3})\s+(?P<line>.+)$", line)
                if match:
                    # If we had sources, save them
                    if sources:
                        res[prefix] = sources
                    sources = []
                    source = {}
                    prefix = match.group("prefix")
                    line = match.group("line")

                #
                # Grab a ROA route table entry
                #
                match = re.match(
                    r"^\-(?P<max>[0-9]+)\s+AS(?P<asn>[0-9]+)"
                    r"\s+\[(?P<protocol>\S+) " + _SINCE_MATCH + r"\] "
                    r"(?:(?P<bestpath>\*) )?"
                    r"\((?P<pref>\d+)\)$",
                    line,
                )
                if match:
                    source = {
                        "ROA.max": int(match.group("max")),
                        "ROA.asn": match.group("asn"),
                        "protocol": match.group("protocol"),
                        "since": match.group("since"),
                        "pref": int(match.group("pref")),
                    }
                    # Check if we have a bestpath
                    bestpath = match.group("bestpath")
                    if bestpath:
                        source["bestpath"] = True
                    else:
                        source["bestpath"] = False
                    # Add source
                    sources.append(source)
                    continue

                #
                # Grab a "normal" route
                #
                match = re.match(
                    r"^(?P<prefix_type>[a-z]+) "
                    r"\[(?P<protocol>\S+) " + _SINCE_MATCH + r"\] "
                    r"(?:(?P<bestpath>\*) )?"
                    r"\((?P<pref>\d+)\)$",
                    line,
                )
                if match:
                    source = {
                        "prefix_type": match.group("prefix_type"),
                        "protocol": match.group("protocol"),
                        "since": match.group("since"),
                        "pref": int(match.group("pref")),
                    }
                    # Check if we have a bestpath
                    bestpath = match.group("bestpath")
                    if bestpath:
                        source["bestpath"] = True
                    else:
                        source["bestpath"] = False
                    # Add source
                    sources.append(source)
                    continue

                #
                # Grab a BGP route
                #
                match = re.match(
                    r"^(?P<prefix_type>[a-z]+) "
                    r"\["
                    r"(?P<protocol>\S+) " + _SINCE_MATCH + r"(?: from (?P<from>[a-z0-9\.:]+))?"
                    r"\] "
                    r"(?:(?P<bestpath>\*) )?"
                    r"\((?P<pref>\d+)(?:/(?P<metric>\d+|[-?]))?\) "
                    r"\["
                    r"(?P<asn>AS[0-9]+)?"
                    r"(?P<bgp_type>[ie\?])"
                    r"\]$",
                    line,
                )
                if match:
                    source = {
                        "prefix_type": match.group("prefix_type"),
                        "protocol": match.group("protocol"),
                        "since": match.group("since"),
                    }
                    # Check if we got a 'from'
                    bgp_from = match.group("from")
                    if bgp_from:
                        source["from"] = bgp_from
                    # Check if we are the bestpath
                    bestpath = match.group("bestpath")
                    if bestpath:
                        source["bestpath"] = True
                    else:
                        source["bestpath"] = False

                    source["pref"] = int(match.group("pref"))
                    # Check if we got a metric
                    metric = match.group("metric")
                    if metric:
                        if metric in ("-", "?"):
                            source["metric"] = None
                        else:
                            source["metric"] = int(metric)
                    # Check if we got an ASN
                    asn = match.group("asn")
                    if asn:
                        source["asn"] = asn
                    source["bgp_type"] = match.group("bgp_type")
                    # Add source
                    sources.append(source)
                    continue

                #
                # Grab a OSPF route
                #
                match = re.match(
                    r"^(?P<prefix_type>[a-z]+) "
                    r"\[(?P<protocol>\S+)\s+" + _SINCE_MATCH + r"\] "
                    r"(?:(?P<bestpath>\*) )?"
                    r"(?P<ospf_type>(?:I|IA|E1|E2)) "
                    r"\((?P<pref>\d+)/(?P<metric1>\d+)(?:/(?P<metric2>\d+))?\)"
                    r"(?: \[(?P<tag>[0-9a-f]+)\])?"
                    r"(?: \[(?P<router_id>[0-9\.]+)\])$",
                    line,
                )
                if match:
                    source = {
                        "prefix_type": match.group("prefix_type"),
                        "protocol": match.group("protocol"),
                        "since": match.group("since"),
                        "ospf_type": match.group("ospf_type"),
                        "pref": int(match.group("pref")),
                        "metric1": int(match.group("metric1")),
                    }
                    # Check if we have a bestpath
                    bestpath = match.group("bestpath")
                    if bestpath:
                        source["bestpath"] = True
                    else:
                        source["bestpath"] = False
                    # Check if we have a metric2
                    metric2 = match.group("metric2")
                    if metric2:
                        source["metric2"] = int(metric2)
                    # Check if we have a tag
                    tag = match.group("tag")
                    if tag:
                        source["tag"] = tag
                    source["router_id"] = match.group("router_id")
                    # Add source
                    sources.append(source)
                    continue

                #
                # Grab a RIP route
                #
                match = re.match(
                    r"^(?P<prefix_type>[a-z]+) "
                    r"\[(?P<protocol>\S+)\s+" + _SINCE_MATCH + r"\] "
                    r"(?:(?P<bestpath>\*) )?"
                    r"\((?P<pref>\d+)/(?P<metric1>\d+)\)$",
                    line,
                )
                if match:
                    source = {
                        "prefix_type": match.group("prefix_type"),
                        "protocol": match.group("protocol"),
                        "since": match.group("since"),
                        "pref": int(match.group("pref")),
                        "metric1": int(match.group("metric1")),
                    }
                    bestpath = match.group("bestpath")
                    if bestpath:
                        source["bestpath"] = True
                    else:
                        source["bestpath"] = False
                    # Add source
                    sources.append(source)
                    continue

                #
                # Grab nexthop details via a gateway
                #
                match = re.match(
                    r"^\s+via\s+"
                    r"(?P<gateway>\S+)\s+"
                    r"on (?P<interface>\S+)"
                    r"(?: mpls (?P<mpls>[0-9/]+))?"
                    r"(?: (?P<onlink>onlink))?"
                    r"(?: weight (?P<weight>[0-9]+))?$",
                    line,
                )
                if match:
                    nexthop: Dict[str, Any] = {}
                    # Grab gateway
                    gateway = match.group("gateway")
                    if gateway:
                        nexthop["gateway"] = gateway
                    # Grab interface
                    interface = match.group("interface")
                    if interface:
                        nexthop["interface"] = interface
                    # Grab mpls
                    mpls = match.group("mpls")
                    if mpls:
                        nexthop["mpls"] = mpls
                    # Grab onlink
                    onlink = match.group("onlink")
                    if onlink:
                        nexthop["onlink"] = onlink
                    # Grab weight
                    weight = match.group("weight")
                    if weight:
                        nexthop["weight"] = int(weight)
                    # Save nexthops
                    if "nexthops" not in source:
                        source["nexthops"] = []
                    source["nexthops"].append(nexthop)
                    continue

                #
                # Grab nexthop details via a gateway
                #
                match = re.match(
                    r"^\s+via\s+"
                    r"(?P<gateway>\S+)\s+"
                    r"on (?P<interface>\S+)"
                    r"(?: mpls (?P<mpls>[0-9/]+))?"
                    r"(?: (?P<onlink>onlink))?"
                    r"(?: weight (?P<weight>[0-9]+))?$",
                    line,
                )
                if match:
                    nexthop = {}
                    # Grab gateway
                    gateway = match.group("gateway")
                    if gateway:
                        nexthop["gateway"] = gateway
                    # Grab interface
                    interface = match.group("interface")
                    if interface:
                        nexthop["interface"] = interface
                    # Grab mpls
                    mpls = match.group("mpls")
                    if mpls:
                        nexthop["mpls"] = mpls
                    # Grab onlink
                    onlink = match.group("onlink")
                    if onlink:
                        nexthop["onlink"] = onlink
                    # Grab weight
                    weight = match.group("weight")
                    if weight:
                        nexthop["weight"] = int(weight)
                    # Save nexthops
                    if "nexthops" not in source:
                        source["nexthops"] = []
                    source["nexthops"].append(nexthop)
                    continue

                #
                # Grab nexthop details via a device
                #
                match = re.match(
                    r"^\s+dev (?P<interface>\S+)"
                    r"(?: mpls (?P<mpls>[0-9/]+))?"
                    r"(?: (?P<onlink>onlink))?"
                    r"(?: weight (?P<weight>[0-9]+))?$",
                    line,
                )
                if match:
                    nexthop = {
                        "interface": match.group("interface"),
                    }
                    # Check if we got an MPLS item
                    mpls = match.group("mpls")
                    if mpls:
                        nexthop["mpls"] = mpls
                    # Check if we got an onlink option
                    onlink = match.group("onlink")
                    if onlink:
                        nexthop["onlink"] = onlink
                    # Check if we got a weight option
                    weight = match.group("weight")
                    if weight:
                        nexthop["weight"] = int(weight)
                    # Save nexthops
                    if "nexthops" not in source:
                        source["nexthops"] = []
                    source["nexthops"].append(nexthop)
                    continue

            # Type
            if code == "1008":
                match = re.match(r"^\s*Type: (?P<route_type>.+)$", line)
                if match:
                    source["type"] = match.group("route_type").split()
                else:
                    raise BirdClientParseError(f"Failed to parse type: {line}")
                continue

            # Pull off route attributes
            if code == "1012":
                # Check if we match a second line in a multiline attribute
                match = re.match(r"^ \t\t(?P<value>.*)$", line)
                if match:
                    # If we do, we should have an attribute set
                    if not attrib:
                        # If not, throw a parsing error
                        raise BirdClientParseError(f"Failed to parse code 1012: {line}")
                    # Finally if we do, grab the value
                    value = match.group("value")
                else:
                    match = re.match(r"^\s*(?P<attrib>[A-Za-z0-9\._]+): ?(?P<value>.*)$", line)
                    if not match:
                        raise BirdClientParseError(f"Failed to parse code 1012: {line}")
                    attrib = match.group("attrib")
                    value = match.group("value")

                # Check if we have attributes, if not, add
                if "attributes" not in source:
                    source["attributes"] = {}

                # Special case for BGP.as_path
                if attrib == "BGP.as_path":
                    match_all = re.findall(r"(?P<as_path>\d+)\s*", value)
                    # Replace values if we have any
                    value = [int(x) for x in match_all]
                # Special case for BGP.ext_community
                elif attrib == "BGP.ext_community":
                    match_all = re.findall(r"\((?P<c1>(?:ro|rt|generic)),\s*(?P<c2>(?:0x)?\d+),\s*(?P<c3>(?:0x)?\d+)\)\s*", value)
                    value = []
                    if match_all:
                        for x in match_all:
                            if x[0] in ["ro", "rt"]:
                                value.append((x[0], int(x[1]), int(x[2])))
                            else:
                                value.append((x[0], x[1], x[2]))
                # Special case for BGP.large_community
                elif attrib == "BGP.community":
                    match_all = re.findall(r"\((?P<c1>\d+),\s*(?P<c2>\d+)\)\s*", value)
                    value = []
                    if match_all:
                        value.extend([(int(x[0]), int(x[1])) for x in match_all])
                # Special case for BGP.large_community
                elif attrib == "BGP.large_community":
                    match_all = re.findall(r"\((?P<lc1>\d+),\s*(?P<lc2>\d+),\s*(?P<lc3>\d+)\)\s*", value)
                    value = []
                    if match_all:
                        value.extend([(int(x[0]), int(x[1]), int(x[2])) for x in match_all])
                # Special case for basic integers
                elif attrib in ("BGP.local_pref", "Kernel.metric", "OSPF.metric1", "OSPF.metric2", "RIP.metric"):
                    value = int(value)
                # Special case for BGP.next_hop
                elif attrib == "BGP.next_hop":
                    match_all = re.findall(r"(?P<next_hop>\S+)\s*", value)
                    value = list(match_all)
                # Special case for BGP.origin
                elif attrib == "BGP.origin":  # noqa: SIM114
                    # Normal string
                    pass
                # Special case for BGP.originator_id
                elif attrib == "BGP.originator_id":  # noqa: SIM114
                    # Normal string
                    pass
                # Special case for BGP.cluster_list
                elif attrib == "BGP.cluster_list":  # noqa: SIM114
                    # Normal string
                    pass

                # Special case for OSPF.router_id
                elif attrib == "OSPF.router_id":  # noqa: SIM114
                    # Normal string
                    pass
                # Special case for OSPF.tag
                elif attrib == "OSPF.tag":
                    # Tag is hex, so we treat it as a string
                    pass

                # Special case for Kernel.scope
                elif attrib == "Kernel.scope":
                    # Translate kernel scope based on /etc/iproute2/rt_scopes
                    if value == "0":
                        value = "global"
                    elif value == "255":
                        value = "link"
                    elif value == "254":
                        value = "host"
                    elif value == "253":
                        value = "link"
                    elif value == "200":
                        value = "site"
                    else:
                        raise BirdClientParseError(f"Kernel scope '{value}' found and not understood: {line}")
                # Special case for Kernel.source
                elif attrib == "Kernel.source":
                    # Translate kernel source into value
                    # https://github.com/BIRD/bird/blob/master/nest/route.h#L370
                    if value == "0":
                        value = "RTS_DUMMY"
                    elif value == "1":
                        value = "RTS_STATIC"
                    elif value == "2":
                        value = "RTS_INHERIT"
                    elif value == "3":
                        value = "RTS_DEVICE"
                    elif value == "4":
                        value = "RTS_STATIC_DEVICE"
                    elif value == "5":
                        value = "RTS_REDIRECT"
                    elif value == "6":
                        value = "RTS_RIP"
                    elif value == "7":
                        value = "RTS_OSPF"
                    elif value == "8":
                        value = "RTS_OSPF_IA"
                    elif value == "9":
                        value = "RTS_OSPF_EXT1"
                    elif value == "10":
                        value = "RTS_OSPF_EXT2"
                    elif value == "11":
                        value = "RTS_BGP"
                    elif value == "12":
                        value = "RTS_PIPE"
                    elif value == "13":
                        value = "RTS_BABEL"
                    else:
                        raise BirdClientParseError("Unknown 'Kernel.source' attribute")
                # Special case for RIP.tag
                elif attrib == "RIP.tag":
                    # This is a string (HEX)
                    pass
                # NK: Bird quirk with 2.0.11, this is supposed to be hidden
                elif attrib == "RIP.02":
                    continue
                # Finally if we don't understand the attribute
                else:
                    raise BirdClientParseError(f"Failed to parse code 1012 attribute '{attrib}: {line}")

                # Check if we have an attribute value already
                if attrib in source["attributes"]:
                    if isinstance(value, list):
                        source["attributes"][attrib].extend(value)
                    else:
                        raise BirdClientParseError("Value is not a list but has multiple items")
                else:
                    source["attributes"][attrib] = value

                continue

            # Check for errors
            if code.startswith("8") or code.startswith("9"):
                raise BirdClientError(f"BIRD client error: {line}")

            # If we didn't match the line, we need to raise an exception
            raise BirdClientParseError(f"Failed to parse BIRD output: {line}")

        return res

    def query(self, query: Union[str, List[str]]) -> List[str]:  # pragma: no cover
        """Open a socket to the BIRD daemon, send the query and get the response."""

        # Make sure socket file is set and it exists else throw a client error
        if not self._control_socket:
            raise BirdClientError("Failed to find BIRD socket file")
        if not os.path.exists(self._control_socket):
            raise BirdClientError(f"BIRD socket file '{self._control_socket}' does not exist")

        # Create a unix socket
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

        # Connect to the BIRD daemon
        sock.connect(self._control_socket)

        # Build query
        if isinstance(query, list):
            query = " ".join(query)

        # Send the query
        sock.send(f"{query}\n".encode("UTF-8"))

        # Initialize byte array to store what we get back
        data = bytearray()

        # Set timeout just incase
        sock.settimeout(300)

        # Loop while we're not done
        done = False
        while not done:
            chunk = sock.recv(4096)
            data.extend(chunk)
            # If the last bit of data ends us off in a newline, this may be the end of the stream
            if data.endswith(b"\n"):
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

        if self._debug:
            print(f"Bird Reply:\n{data.decode('UTF-8')}")

        # Convert data bytes to a string and split into lines
        return data.decode("UTF-8").splitlines()

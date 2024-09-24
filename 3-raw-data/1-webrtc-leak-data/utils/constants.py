#!/usr/bin/python3
# coding: utf-8
#
# Copyright (C) 2024 Guillaume Nibert <guillaume.nibert@snowpack.eu>,
#                    Sébastien Tixeuil <sebastien.tixeuil@lip6.fr>,
#                    Baptiste Polvé <baptiste.polve@snowpack.eu>,
#                    Nana J. Bakalafoua M'boussi <nana.bakalafoua@snowpack.eu>,
#                    Xuan Son Nguyen <xuanson.nguyen@snowpack.eu>
#
# This file is part of 'Anonymise all pcapng traces' and 'Anonymise all txt files'.
#
# 'Anonymise all pcapng traces' and 'Anonymise all txt files' are free software:
# you can redistribute them and/or modify them under the terms of the GNU General
# Public License as published by the Free Software Foundation, either version 3
# of the License, or any later version.
#
# 'Anonymise all pcapng traces' and 'Anonymise all txt files' are distributed in
# the hope that they will be useful, but WITHOUT ANY WARRANTY; without even the
# implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with 'Anonymise all pcapng traces' and 'Anonymise all txt files' programs.
# If not, see <https://www.gnu.org/licenses/>.

"""Correspondence dictionnaries between non-anonymised and anonymised data

This module contains the non-anonymised values of an address as keys of the dictionnaries and their anonymised version
as values of the dictionnaries
"""

__author__ = "Guillaume Nibert"
__credits__ = ["Sébastien Tixeuil", "Baptiste Polvé", "Nana J. Bakalafoua M'boussi", "Xuan Son Nguyen"]
__license__ = "GNU GPLv3"
__maintainer__ = "Guillaume Nibert"
__email__ = "guillaume.nibert@snowpack.eu"


MAC_ADRESSES = {
    "MAC_ADDRESS_TO_ANONYMISE": "00:00:5e:00:53:02",  # Linux - Ethernet MAC
    "MAC_ADDRESS_TO_ANONYMISE": "00:00:5e:00:53:03",  # Linux - Wi-Fi MAC
    "MAC_ADDRESS_TO_ANONYMISE": "00:00:5e:00:53:02",  # macOS - Ethernet MAC
    "MAC_ADDRESS_TO_ANONYMISE": "00:00:5e:00:53:03",  # macOS - Wi-Fi MAC
    "MAC_ADDRESS_TO_ANONYMISE": "00:00:5e:00:53:02",  # Windows - Ethernet MAC
    "MAC_ADDRESS_TO_ANONYMISE": "00:00:5e:00:53:03",  # Windows - Wi-Fi MAC
    "MAC_ADDRESS_TO_ANONYMISE": "00:00:5e:00:53:11",  # coTURN 1
    "MAC_ADDRESS_TO_ANONYMISE": "00:00:5e:00:53:10",  # coTURN 2
    "MAC_ADDRESS_TO_ANONYMISE": "00:00:5e:00:53:20",  # VPN 1
    "MAC_ADDRESS_TO_ANONYMISE": "00:00:5e:00:53:21",  # VPN 2
    "MAC_ADDRESS_TO_ANONYMISE": "00:00:5e:00:53:30",  # Router 
    "MAC_ADDRESS_TO_ANONYMISE": "00:00:5e:00:53:40"   # Router
}

IPV4_ADDRESSES = {
    # WebRTC Linux client
    "IPV4_ADDRESS_TO_ANONYMISE": "203.0.113.20",   # Ethernet IPv4
    "IPV4_ADDRESS_TO_ANONYMISE": "203.0.113.255",  # Ethernet Broadcast IPv4
    "IPV4_ADDRESS_TO_ANONYMISE": "203.0.113.30",   # Wi-Fi IPv4
    "IPV4_ADDRESS_TO_ANONYMISE": "203.0.113.255",  # Wi-Fi Broadcast IPv4
    # macOS
    "IPV4_ADDRESS_TO_ANONYMISE": "203.0.113.20",   # Ethernet IPv4
    "IPV4_ADDRESS_TO_ANONYMISE": "203.0.113.30",   # Wi-Fi IPv4
    # Windows
    "IPV4_ADDRESS_TO_ANONYMISE": "203.0.113.20",   # Ethernet IPv4
    "IPV4_ADDRESS_TO_ANONYMISE": "203.0.113.1",    # Ethernet Gateway IPv4
    "IPV4_ADDRESS_TO_ANONYMISE": "203.0.113.30",   # Wi-Fi IPv4
    "IPV4_ADDRESS_TO_ANONYMISE": "203.0.113.30",   # Wi-Fi IPv6
    "IPV4_ADDRESS_TO_ANONYMISE": "203.0.113.1",    # Wi-Fi Gateway IPv4
    # STUN-TURN IPv4
    "IPV4_ADDRESS_TO_ANONYMISE": "192.0.2.1",
    # VPN, SOCKS and HTTP-HTTPS IPv4
    "IPV4_ADDRESS_TO_ANONYMISE": "198.51.100.1",
}

IPV6_ADDRESSES = {
    # WebRTC Linux client
    "IPV6_ADDRESS_TO_ANONYMISE": "2001:db8::20",  # Ethernet IPv6 scope global temporary dynamic
    "IPV6_ADDRESS_TO_ANONYMISE": "2001:db8::21",  # Ethernet IPv6 scope global dynamic mngtmpaddr noprefixroute
    "IPV6_ADDRESS_TO_ANONYMISE": "2001:db8::30",  # Wi-Fi IPv6 scope global temporary dynamic
    "IPV6_ADDRESS_TO_ANONYMISE": "2001:db8::31",  # Wi-Fi IPv6 scope global dynamic mngtmpaddr noprefixroute
    # macOS
    "IPV6_ADDRESS_TO_ANONYMISE": "2001:db8::20",  # Ethernet Temporary IPv6 Address
    "IPV6_ADDRESS_TO_ANONYMISE": "2001:db8::21",  # Ethernet IPv6 Address
    "IPV6_ADDRESS_TO_ANONYMISE": "2001:db8::30",  # Wi-Fi Temporary IPv6 Address
    "IPV6_ADDRESS_TO_ANONYMISE": "2001:db8::31",  # Wi-Fi IPv6 Address
    # Windows
    "IPV6_ADDRESS_TO_ANONYMISE": "2001:db8::20",  # Ethernet Temporary IPv6 Address
    "IPV6_ADDRESS_TO_ANONYMISE": "2001:db8::21",  # Ethernet IPv6 Address
    "IPV6_ADDRESS_TO_ANONYMISE": "2001:db8::30",  # Wi-Fi Temporary IPv6 Address
    "IPV6_ADDRESS_TO_ANONYMISE": "2001:db8::31",  # Wi-Fi IPv6 Address
    # STUN-TURN IPv6
    "IPV6_ADDRESS_TO_ANONYMISE": "2001:db8::1",
    # VPN, SOCKS and HTTP-HTTPS IPv6
    "IPV6_ADDRESS_TO_ANONYMISE": "2001:db8::2",
}

FQDN_ADDRESSES = {
    "FQDN_ADDRESS_TO_ANONYMISE": "coturn.anony.org",
    "FQDN_ADDRESS_TO_ANONYMISE": "anon.ym"
}

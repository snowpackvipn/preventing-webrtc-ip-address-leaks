#!/usr/bin/python3
# coding: utf-8
#
# Anonymise all pcapng traces
# Copyright (C) 2024 Guillaume Nibert <guillaume.nibert@snowpack.eu>,
#                    Sébastien Tixeuil <sebastien.tixeuil@lip6.fr>,
#                    Baptiste Polvé <baptiste.polve@snowpack.eu>,
#                    Nana J. Bakalafoua M'boussi <nana.bakalafoua@snowpack.eu>,
#                    Xuan Son Nguyen <xuanson.nguyen@snowpack.eu>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

"""Anonymise PCAPNG traces

This module contains functions for anonymising Wireshark/TShark traces with IP addresses anonymised according to
RFCs 5737 and 3849. Anonymisation also applies to the STUN layer.
"""

__author__ = "Guillaume Nibert"
__credits__ = ["Sébastien Tixeuil", "Baptiste Polvé", "Nana J. Bakalafoua M'boussi", "Xuan Son Nguyen"]
__license__ = "GNU GPLv3"
__maintainer__ = "Guillaume Nibert"
__email__ = "guillaume.nibert@snowpack.eu"

import os
import binascii
import socket

from constants import MAC_ADRESSES, IPV4_ADDRESSES, IPV6_ADDRESSES, FQDN_ADDRESSES

DEBUG = False


def convert_string_addresses_to_bytes_addresses(string_addresses: dict, addresse_types: str) -> dict:
    """Convert the correspondence dictionnaries between non-anonymised and anonymised data in bytes

    Args:
        string_addresses (dict): correspondence dictionnaries between non-anonymised and anonymised data in string
        addresse_types (str): 'ipv4', 'ipv6', 'fqdn', 'mac'.

    Returns:
        bytes_addresses (dict): correspondence dictionnaries between non-anonymised and anonymised data in bytes
    """

    bytes_addresses = {}

    if addresse_types == "mac":
        for key, value in string_addresses.items():
            bytes_addresses[binascii.unhexlify(key.replace(":",""))] = binascii.unhexlify(value.replace(":",""))
    elif addresse_types == "ipv4":
        for key, value in string_addresses.items():
            bytes_addresses[socket.inet_aton(key)] = socket.inet_aton(value)
    elif addresse_types == "ipv6":
        for key, value in string_addresses.items():
            bytes_addresses[socket.inet_pton(socket.AF_INET6, key)] = socket.inet_pton(socket.AF_INET6, value)
    elif addresse_types == "fqdn":
        for key, value in string_addresses.items():
            bytes_addresses[bytes(key, "utf8")] = bytes(value, "utf8")
    return bytes_addresses


def byte_xor(bytes_1: bytes, bytes_2: bytes) -> bytes:
    """XOR two bytes of the same size

    Args:
        byte_1 (bytes): bytes 1
        byte_2 (bytes): bytes 2

    Returns:
        bytes: xored bytes
    """
    return bytes([_a ^ _b for _a, _b in zip(bytes_1, bytes_2)])


def replace_sequence(pcapng_trace: bytes, old_bytes: bytes, new_bytes: bytes):
    """Replaces the first occurrence of new_bytes in pcapng_trace with new_bytes.

    Args:
        pcapng_trace (bytes): The bytes object to modify.
        new_bytes (bytes): The bytes sequence to replace with.
    """

    # Find the first occurrence of new_bytes
    try:
        replace_start = pcapng_trace.index(old_bytes)
        replace_end = replace_start + len(new_bytes)
    except ValueError:
        # Sequence not found, return original bytes
        pass

    # Replace the sequence with new bytes
    pcapng_trace[replace_start:replace_end] = new_bytes


def anonymise_pcapng_file(filename: str,
                          values_to_replace_ipv4: dict,
                          values_to_replace_ipv6: dict,
                          values_to_replace_address: dict):
    """Anonymise Wireshark/TShark traces with IP addresses according to RFCs 5737 and 3849.

    Args:
        filename (str): pcapng filename
        values_to_replace_ipv4 (dict): IPv4 non-anonymous and anonymous addresses correspondence in bytes
        values_to_replace_ipv6 (dict): IPv6 non-anonymous and anonymous addresses correspondence in bytes
        values_to_replace_address (dict): other values to anonymise in bytes
    """

    all_ipv4 = set(values_to_replace_ipv4.keys())
    all_ipv4.update(set(values_to_replace_ipv4.values()))

    xored_to_replace_ipv4 = {}

    all_ipv6 = set(values_to_replace_ipv6.keys())
    all_ipv6.update(set(values_to_replace_ipv6.values()))

    xored_to_replace_ipv6 = {}

    with open(filename, 'rb') as pcapng_trace:
        pkt_bytes = pcapng_trace.read()

    # Create a list to store modified bytes

    modified_bytes = bytearray(pkt_bytes)

    ip_version_4 = "0100"
    ip_version_6 = "0110"

    # Loop through each byte in the original bytes object
    index = 0

    while index < len(pkt_bytes):

        ip_version_and_header = pkt_bytes[index:index+1]

        # [Internet Protocol Version 4] Version: 4 (0b0100) or [Internet Protocol Version 6] Version: 6 (0b0110)
        ip_version = bin(int.from_bytes(ip_version_and_header, byteorder='big'))[2:5].zfill(4)

        # IPv4 packet
        if (ip_version == ip_version_4
                and pkt_bytes[index+12:index+16] in all_ipv4
                and pkt_bytes[index+16:index+20] in all_ipv4):

            ip_header_lenght = int(bin(int.from_bytes(ip_version_and_header, byteorder='big'))[-4:].zfill(4), 2)*4

            index += ip_header_lenght                    # [Internet Protocol Version 4] Header Length
                                                         # If STUN conveys only a XOR-MAPPED-ADDRESS:
            index += 8                                   # [Session Traversal Utilities for NAT] Message type: 0x0101
                                                         # (Binding Success Response)
            if pkt_bytes[index:index+2] == b'\x01\x01':
                start_stun_message_index = index

                index += 2                               # [Session Traversal Utilities for NAT] Message Length
                index += 2                               # [Session Traversal Utilities for NAT] Message Cookie
                message_cookie = pkt_bytes[index:index+4]
                if DEBUG:
                    print("{} Message Cookie: {}".format(
                        filename,"".join("\\x{:02x}".format(c) for c in message_cookie)
                    ))

                index += 4   # [Session Traversal Utilities for NAT] Message Transaction ID
                index += 12  # [Session Traversal Utilities for NAT] Attribute Type: XOR-MAPPED-ADDRESS
                index += 2   # [Session Traversal Utilities for NAT] Attribute Lenght
                index += 2   # [Session Traversal Utilities for NAT] Reserved
                index += 1   # [Session Traversal Utilities for NAT] Protocol Family (0x01: IPv4; 0x02: IPv6)
                index += 1   # [Session Traversal Utilities for NAT] Port (XOR-d) (XOR-MAPPED-IP-ADDRESS)
                index += 2   # [Session Traversal Utilities for NAT] IP (XOR-d) (XOR-MAPPED-IP-ADDRESS)

                xor_mapped_ip_address = pkt_bytes[index:index+4]
                if DEBUG:
                    print("{} XOR-MAPPED-IP-ADDRESS: {}".format(
                        filename,"".join("\\x{:02x}".format(c) for c in xor_mapped_ip_address)
                    ))

                # Forging a new anonymised XOR-MAPPED-ADDRESS
                if pkt_bytes[index+12:index+16] in values_to_replace_ipv4:
                    new_xor_mapped_ip_address = byte_xor(values_to_replace_ipv4[pkt_bytes[index+12:index+16]],
                                                         message_cookie)
                    modified_bytes[index:index+4] = new_xor_mapped_ip_address
                    xored_to_replace_ipv4[xor_mapped_ip_address] = new_xor_mapped_ip_address

                index += 4  # [Session Traversal Utilities for NAT] Attribute Type: MAPPED-ADDRESS
                index += 2  # [Session Traversal Utilities for NAT] Attribute Lenght
                index += 2  # [Session Traversal Utilities for NAT] Reserved
                index += 1  # [Session Traversal Utilities for NAT] Protocol Family (0x01: IPv4; 0x02: IPv6)
                index += 1  # [Session Traversal Utilities for NAT] Port (MAPPED-IP-ADDRESS)
                index += 2  # [Session Traversal Utilities for NAT] IP (MAPPED-IP-ADDRESS)

                mapped_ip_address = pkt_bytes[index:index+4]

                if mapped_ip_address in values_to_replace_ipv4:
                    modified_bytes[index:index+4] = values_to_replace_ipv4[mapped_ip_address]

                index += 4  # [Session Traversal Utilities for NAT] Attribute Type: RESPONSE-ORIGIN
                index += 2  # [Session Traversal Utilities for NAT] Attribute Lenght
                index += 2  # [Session Traversal Utilities for NAT] Reserved
                index += 1  # [Session Traversal Utilities for NAT] Protocol Family (0x01: IPv4; 0x02: IPv6)
                index += 1  # [Session Traversal Utilities for NAT] Port (RESPONSE-ORIGIN)
                index += 2  # [Session Traversal Utilities for NAT] IP (RESPONSE-ORIGIN)

                response_origin_address = pkt_bytes[index:index+4]

                if response_origin_address in values_to_replace_ipv4:
                    modified_bytes[index:index+4] = values_to_replace_ipv4[response_origin_address]

                index += 4  # [Session Traversal Utilities for NAT] Attribute Type: OTHER-ADDRESS
                index += 2  # [Session Traversal Utilities for NAT] Attribute Lenght
                index += 2  # [Session Traversal Utilities for NAT] Reserved
                index += 1  # [Session Traversal Utilities for NAT] Protocol Family (0x01: IPv4; 0x02: IPv6)
                index += 1  # [Session Traversal Utilities for NAT] Port (OTHER-ADDRESS)
                index += 2  # [Session Traversal Utilities for NAT] IP (OTHER-ADDRESS)

                other_address = pkt_bytes[index:index+4]

                if other_address in values_to_replace_ipv4:
                    modified_bytes[index:index+4] = values_to_replace_ipv4[other_address]

                index += 4  # [Session Traversal Utilities for NAT] Attribute type: SOFTWARE (0x8022)
                if pkt_bytes[index:index+2] == b'\x80\x22':
                    index += 2  # [Session Traversal Utilities for NAT] Attribute Length
                    software_attribute_lenght = int.from_bytes(pkt_bytes[index:index+2], 'big')
                    index += 2  # [Session Traversal Utilities for NAT] Software

                    # [Session Traversal Utilities for NAT] Attribute Type: FINGERPRINT
                    index += software_attribute_lenght

                    fingerprintable_stun_message_index = index

                # [Session Traversal Utilities for NAT] Attribute type: FINGERPRINT (0x8028)
                if pkt_bytes[index:index+2] == b'\x80\x28':
                    index += 2  # [Session Traversal Utilities for NAT] Attribute Length
                    index += 2  # [Session Traversal Utilities for NAT] CRC-32

                    # RFC 8489 - Session Traversal Utilities for NAT (STUN) - Section 14.7 FINGERPRINT
                    # "[...] The value of the attribute is computed as the CRC-32 of the STUN message up to (but
                    # excluding) the FINGERPRINT attribute itself, XOR'ed with the 32-bit value 0x5354554e. [...]"
                    # https://datatracker.ietf.org/doc/html/rfc8489#section-14.7
                    new_crc32_ituv42 = byte_xor(
                        binascii.crc32(
                            pkt_bytes[start_stun_message_index:fingerprintable_stun_message_index]).to_bytes(4, 'big'),
                        b'\x53\x54\x55\x4e'
                    )

                    modified_bytes[index:index+4] = new_crc32_ituv42

                                                           # If STUN conveys in addition a XOR-RELAYED-ADDRESS:
                                                           # [Session Traversal Utilities for NAT] Message type: 0x0103
            elif pkt_bytes[index:index+2] == b'\x01\x03':  # (Allocate Success Response)
                start_stun_message_index = index

                index += 2                                 # [Session Traversal Utilities for NAT] Message Length
                index += 2                                 # [Session Traversal Utilities for NAT] Message Cookie
                message_cookie = pkt_bytes[index:index+4]
                if DEBUG:
                    print("{} Message Cookie: {}".format(
                        filename, "".join("\\x{:02x}".format(c) for c in message_cookie)
                    ))

                index += 4   # [Session Traversal Utilities for NAT] Message Transaction ID
                message_transaction_id = pkt_bytes[index:index+12]
                if DEBUG:
                    print("{} Message Transaction ID: {}".format(
                        filename, "".join("\\x{:02x}".format(c) for c in message_transaction_id)
                    ))

                index += 12  # [Session Traversal Utilities for NAT] Attribute Type: XOR-RELAYED-ADDRESS
                index += 2   # [Session Traversal Utilities for NAT] Attribute Lenght
                index += 2   # [Session Traversal Utilities for NAT] Reserved
                index += 1   # [Session Traversal Utilities for NAT] Protocol Family (0x01: IPv4; 0x02: IPv6)
                protocol_family = pkt_bytes[index:index+1]

                index += 1   # [Session Traversal Utilities for NAT] Port (XOR-d) (XOR-RELAYED-IP-ADDRESS)
                index += 2   # [Session Traversal Utilities for NAT] IP (XOR-d) (XOR-RELAYED-IP-ADDRESS)

                if protocol_family == b'\x01':  # IPv4
                    xor_relayed_ip_address = pkt_bytes[index:index+4]
                    if DEBUG:
                        print("{} XOR-RELAYED-IP-ADDRESS: {}".format(
                            filename, "".join("\\x{:02x}".format(c) for c in xor_relayed_ip_address)
                        ))

                    relayed_ip_address = byte_xor(message_cookie, xor_relayed_ip_address)
                    # Forging a new anonymised IPv4 XOR-RELAYED-ADDRESS
                    if relayed_ip_address in values_to_replace_ipv4:
                        new_xor_relayed_ip_address = byte_xor(values_to_replace_ipv4[relayed_ip_address],
                                                              message_cookie)
                        modified_bytes[index:index+4] = new_xor_relayed_ip_address
                        xored_to_replace_ipv4[xor_relayed_ip_address] = new_xor_relayed_ip_address

                    index += 4   # [Session Traversal Utilities for NAT] Attribute Type: XOR-MAPPED-ADDRESS

                elif protocol_family == b'\x02':  # IPv6
                    xor_relayed_ip_address = pkt_bytes[index:index+16]
                    if DEBUG:
                        print("{} XOR-RELAYED-IP-ADDRESS: {}".format(
                            filename, "".join("\\x{:02x}".format(c) for c in xor_relayed_ip_address)
                        ))

                    relayed_ip_address = byte_xor(message_cookie + message_transaction_id, xor_relayed_ip_address)
                    # Forging a new anonymised IPv6 XOR-RELAYED-ADDRESS
                    if relayed_ip_address in values_to_replace_ipv6:
                        new_xor_relayed_ip_address = byte_xor(values_to_replace_ipv6[relayed_ip_address],
                                                              message_cookie + message_transaction_id)
                        modified_bytes[index:index+16] = new_xor_relayed_ip_address
                        xored_to_replace_ipv6[xor_relayed_ip_address] = new_xor_relayed_ip_address

                    index += 16  # [Session Traversal Utilities for NAT] Attribute Type: XOR-MAPPED-ADDRESS

                index += 2   # [Session Traversal Utilities for NAT] Attribute Lenght
                index += 2   # [Session Traversal Utilities for NAT] Reserved
                index += 1   # [Session Traversal Utilities for NAT] Protocol Family (0x01: IPv4; 0x02: IPv6)
                index += 1   # [Session Traversal Utilities for NAT] Port (XOR-d) (XOR-MAPPED-IP-ADDRESS)
                index += 2   # [Session Traversal Utilities for NAT] IP (XOR-d) (XOR-MAPPED-IP-ADDRESS)

                xor_mapped_ip_address = pkt_bytes[index:index+4]

                mapped_ip_address = byte_xor(message_cookie, xor_mapped_ip_address)
                if DEBUG:
                    print("{} XOR-MAPPED-IP-ADDRESS: {}".format(
                        filename, "".join("\\x{:02x}".format(c) for c in xor_mapped_ip_address)
                    ))

                if mapped_ip_address in values_to_replace_ipv4:
                    new_xor_mapped_ip_address = byte_xor(values_to_replace_ipv4[mapped_ip_address], message_cookie)
                    modified_bytes[index:index+4] = new_xor_mapped_ip_address
                    xored_to_replace_ipv4[xor_mapped_ip_address] = new_xor_mapped_ip_address

                index += 4  # [Session Traversal Utilities for NAT] Attribute type: LIFETIME (0x000d)
                if pkt_bytes[index:index+2] == b'\x00\x0d':
                    index += 2  # [Session Traversal Utilities for NAT] Attribute Length
                    index += 2  # [Session Traversal Utilities for NAT] Lifetime

                index += 4  # [Session Traversal Utilities for NAT] Attribute type: SOFTWARE (0x8022)
                if pkt_bytes[index:index+2] == b'\x80\x22':
                    index += 2  # [Session Traversal Utilities for NAT] Attribute Length
                    software_attribute_lenght = int.from_bytes(pkt_bytes[index:index+2], 'big')
                    index += 2  # [Session Traversal Utilities for NAT] Software

                    # [Session Traversal Utilities for NAT] Attribute Type: MESSAGE-INTEGRITY
                    index += software_attribute_lenght
                if pkt_bytes[index:index+2] == b'\x00\x08':
                    index += 2  # [Session Traversal Utilities for NAT] Attribute Length
                    index += 2  # [Session Traversal Utilities for NAT] HMAC-SHA1
                    index += 20 # [Session Traversal Utilities for NAT] Attribute Type: FINGERPRINT

                    fingerprintable_stun_message_index = index

                # [Session Traversal Utilities for NAT] Attribute type: FINGERPRINT (0x8028)
                if pkt_bytes[index:index+2] == b'\x80\x28':
                    index += 2  # [Session Traversal Utilities for NAT] Attribute Length
                    index += 2  # [Session Traversal Utilities for NAT] CRC-32

                    # RFC 8489 - Session Traversal Utilities for NAT (STUN) - Section 14.7 FINGERPRINT
                    # "[...] The value of the attribute is computed as the CRC-32 of the STUN message up to (but
                    # excluding) the FINGERPRINT attribute itself, XOR'ed with the 32-bit value 0x5354554e. [...]"
                    # https://datatracker.ietf.org/doc/html/rfc8489#section-14.7
                    new_crc32_ituv42 = byte_xor(
                        binascii.crc32(
                            pkt_bytes[start_stun_message_index:fingerprintable_stun_message_index]).to_bytes(4, 'big'),
                        b'\x53\x54\x55\x4e'
                    )

                    modified_bytes[index:index+4] = new_crc32_ituv42

            # [Session Traversal Utilities for NAT] Message type: 0x0113 (Allocate Error Response)
            elif pkt_bytes[index:index+2] == b'\x01\x13':
                start_stun_message_index = index

                index += 2   # [Session Traversal Utilities for NAT] Message Length
                index += 2   # [Session Traversal Utilities for NAT] Message Cookie
                index += 4   # [Session Traversal Utilities for NAT] Message Transaction ID
                index += 12  # [Session Traversal Utilities for NAT] ERROR-CODE 401 (unauthenticated): Unauthorized

                index += 60  # [Session Traversal Utilities for NAT] NONCE and REALM


                # [Session Traversal Utilities for NAT] Attribute type: SOFTWARE (0x8022)
                if pkt_bytes[index:index+2] == b'\x80\x22':

                    index += 2  # [Session Traversal Utilities for NAT] Attribute Length
                    software_attribute_lenght = int.from_bytes(pkt_bytes[index:index+2], 'big')
                    index += 2  # [Session Traversal Utilities for NAT] Software

                    # [Session Traversal Utilities for NAT] Attribute Type: FINGERPRINT
                    index += software_attribute_lenght

                    fingerprintable_stun_message_index = index

                # [Session Traversal Utilities for NAT] Attribute type: FINGERPRINT (0x8028)
                if pkt_bytes[index:index+2] == b'\x80\x28':
                    index += 2  # [Session Traversal Utilities for NAT] Attribute Length
                    index += 2  # [Session Traversal Utilities for NAT] CRC-32

                    # RFC 8489 - Session Traversal Utilities for NAT (STUN) - Section 14.7 FINGERPRINT
                    # "[...] The value of the attribute is computed as the CRC-32 of the STUN message up to (but
                    # excluding) the FINGERPRINT attribute itself, XOR'ed with the 32-bit value 0x5354554e. [...]"
                    # https://datatracker.ietf.org/doc/html/rfc8489#section-14.7
                    new_crc32_ituv42 = byte_xor(
                        binascii.crc32(
                            pkt_bytes[start_stun_message_index:fingerprintable_stun_message_index]).to_bytes(4, 'big'),
                        b'\x53\x54\x55\x4e'
                    )

                    modified_bytes[index:index+4] = new_crc32_ituv42


        elif (ip_version == ip_version_6
                and pkt_bytes[index+8:index+24] in all_ipv6
                and pkt_bytes[index+24:index+40] in all_ipv6):
            ip_header_lenght = 40
            index += ip_header_lenght                    # [Internet Protocol Version 6] Header Length

                                                         # If STUN conveys only a XOR-MAPPED-ADDRESS:
            index +=  8                                  # [Session Traversal Utilities for NAT] Message type: 0x0101
                                                         # (Binding Success Response)
            if pkt_bytes[index:index+2] == b'\x01\x01':
                start_stun_message_index = index

                index += 2                               # [Session Traversal Utilities for NAT] Message Length
                index += 2                               # [Session Traversal Utilities for NAT] Message Cookie

                message_cookie = pkt_bytes[index:index+4]
                if DEBUG:
                    print("{} Message Cookie: {}".format(
                        filename, "".join("\\x{:02x}".format(c) for c in message_cookie)
                    ))

                index += 4   # [Session Traversal Utilities for NAT] Message Transaction ID
                message_transaction_id = pkt_bytes[index:index+12]
                if DEBUG:
                    print("{} Message Transaction ID: {}".format(
                        filename, "".join("\\x{:02x}".format(c) for c in message_transaction_id)
                    ))

                index += 12  # [Session Traversal Utilities for NAT] Attribute Type: XOR-MAPPED-ADDRESS
                index += 2   # [Session Traversal Utilities for NAT] Attribute Lenght
                index += 2   # [Session Traversal Utilities for NAT] Reserved
                index += 1   # [Session Traversal Utilities for NAT] Protocol Family (0x01: IPv4; 0x02: IPv6)
                index += 1   # [Session Traversal Utilities for NAT] Port (XOR-d) (XOR-MAPPED-IP-ADDRESS)
                index += 2   # [Session Traversal Utilities for NAT] IP (XOR-d) (XOR-MAPPED-IP-ADDRESS)

                xor_mapped_ip_address = pkt_bytes[index:index+16]
                if DEBUG:
                    print("{} XOR-MAPPED-IP-ADDRESS: {}".format(
                        filename, "".join("\\x{:02x}".format(c) for c in xor_mapped_ip_address)
                    ))

                # Forging a new anonymised XOR-MAPPED-ADDRESS
                if pkt_bytes[index+24:index+40] in values_to_replace_ipv6:
                    new_xor_mapped_ip_address = byte_xor(values_to_replace_ipv6[pkt_bytes[index+24:index+40]],
                                                         message_cookie + message_transaction_id)
                    modified_bytes[index:index+16] = new_xor_mapped_ip_address
                    xored_to_replace_ipv6[xor_mapped_ip_address] = new_xor_mapped_ip_address

                index += 16  # [Session Traversal Utilities for NAT] Attribute Type: MAPPED-ADDRESS
                index += 2   # [Session Traversal Utilities for NAT] Attribute Lenght
                index += 2   # [Session Traversal Utilities for NAT] Reserved
                index += 1   # [Session Traversal Utilities for NAT] Protocol Family (0x01: IPv4; 0x02: IPv6)
                index += 1   # [Session Traversal Utilities for NAT] Port (MAPPED-IP-ADDRESS)
                index += 2   # [Session Traversal Utilities for NAT] IP (MAPPED-IP-ADDRESS)

                mapped_ip_address = pkt_bytes[index:index+16]

                if mapped_ip_address in values_to_replace_ipv6:
                    modified_bytes[index:index+16] = values_to_replace_ipv6[mapped_ip_address]

                index += 16  # [Session Traversal Utilities for NAT] Attribute Type: RESPONSE-ORIGIN
                index += 2   # [Session Traversal Utilities for NAT] Attribute Lenght
                index += 2   # [Session Traversal Utilities for NAT] Reserved
                index += 1   # [Session Traversal Utilities for NAT] Protocol Family (0x01: IPv4; 0x02: IPv6)
                index += 1   # [Session Traversal Utilities for NAT] Port (RESPONSE-ORIGIN)
                index += 2   # [Session Traversal Utilities for NAT] IP (RESPONSE-ORIGIN)

                response_origin_address = pkt_bytes[index:index+16]

                if response_origin_address in values_to_replace_ipv6:
                    modified_bytes[index:index+16] = values_to_replace_ipv6[response_origin_address]

                index += 16  # [Session Traversal Utilities for NAT] Attribute Type: OTHER-ADDRESS
                index += 2   # [Session Traversal Utilities for NAT] Attribute Lenght
                index += 2   # [Session Traversal Utilities for NAT] Reserved
                index += 1   # [Session Traversal Utilities for NAT] Protocol Family (0x01: IPv4; 0x02: IPv6)
                index += 1   # [Session Traversal Utilities for NAT] Port (OTHER-ADDRESS)
                index += 2   # [Session Traversal Utilities for NAT] IP (OTHER-ADDRESS)

                other_address = pkt_bytes[index:index+16]

                if other_address in values_to_replace_ipv6:
                    modified_bytes[index:index+16] = values_to_replace_ipv6[other_address]

                index += 16 # [Session Traversal Utilities for NAT] Attribute type: SOFTWARE (0x8022)
                if pkt_bytes[index:index+2] == b'\x80\x22':
                    index += 2  # [Session Traversal Utilities for NAT] Attribute Length
                    software_attribute_lenght = int.from_bytes(pkt_bytes[index:index+2], 'big')
                    index += 2  # [Session Traversal Utilities for NAT] Software

                    # [Session Traversal Utilities for NAT] Attribute Type: FINGERPRINT
                    index += software_attribute_lenght

                    fingerprintable_stun_message_index = index

                # [Session Traversal Utilities for NAT] Attribute type: FINGERPRINT (0x8028)
                if pkt_bytes[index:index+2] == b'\x80\x28':
                    index += 2  # [Session Traversal Utilities for NAT] Attribute Length
                    index += 2  # [Session Traversal Utilities for NAT] CRC-32

                    # RFC 8489 - Session Traversal Utilities for NAT (STUN) - Section 14.7 FINGERPRINT
                    # "[...] The value of the attribute is computed as the CRC-32 of the STUN message up to (but
                    # excluding) the FINGERPRINT attribute itself, XOR'ed with the 32-bit value 0x5354554e. [...]"
                    # https://datatracker.ietf.org/doc/html/rfc8489#section-14.7
                    new_crc32_ituv42 = byte_xor(
                        binascii.crc32(
                            pkt_bytes[start_stun_message_index:fingerprintable_stun_message_index]).to_bytes(4, 'big'),
                        b'\x53\x54\x55\x4e'
                    )

                    modified_bytes[index:index+4] = new_crc32_ituv42

                                                           # If STUN conveys in addition a XOR-RELAYED-ADDRESS:
                                                           # [Session Traversal Utilities for NAT] Message type: 0x0103
            elif pkt_bytes[index:index+2] == b'\x01\x03':  # (Allocate Success Response)
                start_stun_message_index = index

                index += 2                                 # [Session Traversal Utilities for NAT] Message Length
                index += 2                                 # [Session Traversal Utilities for NAT] Message Cookie
                message_cookie = pkt_bytes[index:index+4]
                if DEBUG:
                    print("{} Message Cookie: {}".format(
                        filename, "".join("\\x{:02x}".format(c) for c in message_cookie)
                    ))

                index += 4   # [Session Traversal Utilities for NAT] Message Transaction ID
                message_transaction_id = pkt_bytes[index:index+12]
                if DEBUG:
                    print("{} Message Transaction ID: {}".format(
                        filename, "".join("\\x{:02x}".format(c) for c in message_transaction_id)
                    ))

                index += 12  # [Session Traversal Utilities for NAT] Attribute Type: XOR-RELAYED-ADDRESS
                index += 2   # [Session Traversal Utilities for NAT] Attribute Lenght
                index += 2   # [Session Traversal Utilities for NAT] Reserved
                index += 1   # [Session Traversal Utilities for NAT] Protocol Family (0x01: IPv4; 0x02: IPv6)
                protocol_family = pkt_bytes[index:index+1]

                index += 1   # [Session Traversal Utilities for NAT] Port (XOR-d) (XOR-RELAYED-IP-ADDRESS)
                index += 2   # [Session Traversal Utilities for NAT] IP (XOR-d) (XOR-RELAYED-IP-ADDRESS)

                if protocol_family == b'\x01':  # IPv4
                    xor_relayed_ip_address = pkt_bytes[index:index+4]
                    if DEBUG:
                        print("{} XOR-RELAYED-IP-ADDRESS: {}".format(
                            filename, "".join("\\x{:02x}".format(c) for c in xor_relayed_ip_address)
                        ))

                    relayed_ip_address = byte_xor(message_cookie, xor_relayed_ip_address)
                    # Forging a new anonymised IPv4 XOR-RELAYED-ADDRESS
                    if relayed_ip_address in values_to_replace_ipv4:
                        new_xor_relayed_ip_address = byte_xor(values_to_replace_ipv4[relayed_ip_address],
                                                              message_cookie)
                        modified_bytes[index:index+4] = new_xor_relayed_ip_address
                        xored_to_replace_ipv4[xor_relayed_ip_address] = new_xor_relayed_ip_address

                    index += 4   # [Session Traversal Utilities for NAT] Attribute Type: XOR-MAPPED-ADDRESS

                elif protocol_family == b'\x02':  # IPv6
                    xor_relayed_ip_address = pkt_bytes[index:index+16]
                    if DEBUG:
                        print("{} XOR-RELAYED-IP-ADDRESS: {}".format(
                            filename, "".join("\\x{:02x}".format(c) for c in xor_relayed_ip_address)
                        ))

                    relayed_ip_address = byte_xor(message_cookie + message_transaction_id, xor_relayed_ip_address)
                    # Forging a new anonymised IPv6 XOR-RELAYED-ADDRESS
                    if relayed_ip_address in values_to_replace_ipv6:
                        new_xor_relayed_ip_address = byte_xor(values_to_replace_ipv6[relayed_ip_address],
                                                              message_cookie + message_transaction_id)
                        modified_bytes[index:index+16] = new_xor_relayed_ip_address
                        xored_to_replace_ipv6[xor_relayed_ip_address] = new_xor_relayed_ip_address

                    index += 16  # [Session Traversal Utilities for NAT] Attribute Type: XOR-MAPPED-ADDRESS

                index += 2       # [Session Traversal Utilities for NAT] Attribute Lenght
                index += 2       # [Session Traversal Utilities for NAT] Reserved
                index += 1       # [Session Traversal Utilities for NAT] Protocol Family (0x01: IPv4; 0x02: IPv6)
                index += 1       # [Session Traversal Utilities for NAT] Port (XOR-d) (XOR-MAPPED-IP-ADDRESS)
                index += 2       # [Session Traversal Utilities for NAT] IP (XOR-d) (XOR-MAPPED-IP-ADDRESS)

                xor_mapped_ip_address = pkt_bytes[index:index+16]

                mapped_ip_address = byte_xor(message_cookie + message_transaction_id, xor_mapped_ip_address)
                if DEBUG:
                    print("{} XOR-MAPPED-IP-ADDRESS: {}".format(
                        filename, "".join("\\x{:02x}".format(c) for c in xor_mapped_ip_address)
                    ))

                if mapped_ip_address in values_to_replace_ipv6:
                    new_xor_mapped_ip_address = byte_xor(values_to_replace_ipv6[mapped_ip_address],
                                                         message_cookie + message_transaction_id)
                    modified_bytes[index:index+16] = new_xor_mapped_ip_address
                    xored_to_replace_ipv6[xor_mapped_ip_address] = new_xor_mapped_ip_address

                index += 16  # [Session Traversal Utilities for NAT] Attribute type: LIFETIME (0x000d)
                if pkt_bytes[index:index+2] == b'\x00\x0d':
                    index += 2  # [Session Traversal Utilities for NAT] Attribute Length
                    index += 2  # [Session Traversal Utilities for NAT] Lifetime

                index += 4  # [Session Traversal Utilities for NAT] Attribute type: SOFTWARE (0x8022)
                if pkt_bytes[index:index+2] == b'\x80\x22':
                    index += 2  # [Session Traversal Utilities for NAT] Attribute Length
                    software_attribute_lenght = int.from_bytes(pkt_bytes[index:index+2], 'big')
                    index += 2  # [Session Traversal Utilities for NAT] Software

                    # [Session Traversal Utilities for NAT] Attribute Type: MESSAGE-INTEGRITY
                    index += software_attribute_lenght

                if pkt_bytes[index:index+2] == b'\x00\x08':

                    index += 2  # [Session Traversal Utilities for NAT] Attribute Length
                    index += 2  # [Session Traversal Utilities for NAT] HMAC-SHA1
                    index += 20 # [Session Traversal Utilities for NAT] Attribute Type: FINGERPRINT

                    fingerprintable_stun_message_index = index

                # [Session Traversal Utilities for NAT] Attribute type: FINGERPRINT (0x8028)
                if pkt_bytes[index:index+2] == b'\x80\x28':

                    index += 2  # [Session Traversal Utilities for NAT] Attribute Length
                    index += 2  # [Session Traversal Utilities for NAT] CRC-32

                    # RFC 8489 - Session Traversal Utilities for NAT (STUN) - Section 14.7 FINGERPRINT
                    # "[...] The value of the attribute is computed as the CRC-32 of the STUN message up to (but
                    # excluding) the FINGERPRINT attribute itself, XOR'ed with the 32-bit value 0x5354554e. [...]"
                    # https://datatracker.ietf.org/doc/html/rfc8489#section-14.7
                    new_crc32_ituv42 = byte_xor(
                        binascii.crc32(
                            pkt_bytes[start_stun_message_index:fingerprintable_stun_message_index]).to_bytes(4, 'big'),
                        b'\x53\x54\x55\x4e'
                    )

                    modified_bytes[index:index+4] = new_crc32_ituv42

            # [Session Traversal Utilities for NAT] Message type: 0x0113 (Allocate Error Response)
            elif pkt_bytes[index:index+2] == b'\x01\x13':
                start_stun_message_index = index

                index += 2   # [Session Traversal Utilities for NAT] Message Length
                index += 2   # [Session Traversal Utilities for NAT] Message Cookie
                index += 4   # [Session Traversal Utilities for NAT] Message Transaction ID
                index += 12  # [Session Traversal Utilities for NAT] ERROR-CODE 401 (unauthenticated): Unauthorized

                index += 60  # [Session Traversal Utilities for NAT] NONCE and REALM

                # [Session Traversal Utilities for NAT] Attribute type: SOFTWARE (0x8022)
                if pkt_bytes[index:index+2] == b'\x80\x22':
                    index += 2  # [Session Traversal Utilities for NAT] Attribute Length
                    software_attribute_lenght = int.from_bytes(pkt_bytes[index:index+2], 'big')
                    index += 2  # [Session Traversal Utilities for NAT] Software

                    # [Session Traversal Utilities for NAT] Attribute Type: FINGERPRINT
                    index += software_attribute_lenght

                    fingerprintable_stun_message_index = index

                # [Session Traversal Utilities for NAT] Attribute type: FINGERPRINT (0x8028)
                if pkt_bytes[index:index+2] == b'\x80\x28':
                    index += 2  # [Session Traversal Utilities for NAT] Attribute Length
                    index += 2  # [Session Traversal Utilities for NAT] CRC-32

                    # RFC 8489 - Session Traversal Utilities for NAT (STUN) - Section 14.7 FINGERPRINT
                    # "[...] The value of the attribute is computed as the CRC-32 of the STUN message up to (but
                    # excluding) the FINGERPRINT attribute itself, XOR'ed with the 32-bit value 0x5354554e. [...]"
                    # https://datatracker.ietf.org/doc/html/rfc8489#section-14.7
                    new_crc32_ituv42 = byte_xor(
                        binascii.crc32(
                            pkt_bytes[start_stun_message_index:fingerprintable_stun_message_index]).to_bytes(4, 'big'),
                        b'\x53\x54\x55\x4e'
                    )

                    modified_bytes[index:index+4] = new_crc32_ituv42

        index += 1


    # Anonymise other layers of the TCP/IP stack
    for non_anonymised_realm, anonymised_realm in values_to_replace_address.items():
        while non_anonymised_realm in modified_bytes:
            print(f"{filename} - Realm adress: {non_anonymised_realm}")
            replace_sequence(modified_bytes, non_anonymised_realm, anonymised_realm)

    for non_anonymised_ip_addr, anonymised_ip_addr in values_to_replace_ipv4.items():
        while non_anonymised_ip_addr in modified_bytes:
            print(f"{filename} - IPv4 adress: {non_anonymised_ip_addr}")
            replace_sequence(modified_bytes, non_anonymised_ip_addr, anonymised_ip_addr)

    for non_anonymised_xored_ip_addr, anonymised_ip_xored_addr in xored_to_replace_ipv4.items():
        while non_anonymised_xored_ip_addr in modified_bytes:
            print(f"{filename} - XORED IPv4 adress: {non_anonymised_xored_ip_addr}")
            replace_sequence(modified_bytes, non_anonymised_xored_ip_addr, anonymised_ip_xored_addr)

    for non_anonymised_ip_addr, anonymised_ip_addr in values_to_replace_ipv6.items():
        while non_anonymised_ip_addr in modified_bytes:
            print(f"{filename} - IPv6 adress: {non_anonymised_ip_addr}")
            replace_sequence(modified_bytes, non_anonymised_ip_addr, anonymised_ip_addr)

    for non_anonymised_xored_ip_addr, anonymised_ip_xored_addr in xored_to_replace_ipv6.items():
        while non_anonymised_xored_ip_addr in modified_bytes:
            print(f"{filename} - XORED IPv6 adress: {non_anonymised_xored_ip_addr}")
            replace_sequence(modified_bytes, non_anonymised_xored_ip_addr, anonymised_ip_xored_addr)

    newbytes = bytes(modified_bytes)

    with open(filename, "wb") as anonymised_pcapng_trace:
        # Update the file
        anonymised_pcapng_trace.write(newbytes)


def walk_and_replace(directory: str,
                     bytes_ipv4_addresses: dict,
                     bytes_ipv6_addresses: dict,
                     other_values_to_replace: dict):
    """Walks through a directory and recursively applies `parse_and_replace_values` to all .txt files.

    Args:
        directory (str): The path to the directory to start searching from.
        bytes_ipv4_addresses (dict): IPv4 non-anonymous and anonymous addresses correspondence in bytes
        bytes_ipv6_addresses (dict): IPv6 non-anonymous and anonymous addresses correspondence in bytes
        other_values_to_replace (dict): other values to anonymise in bytes
    """

    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".pcapng"):
                filepath = os.path.join(root, filename)
                anonymise_pcapng_file(filepath, bytes_ipv4_addresses, bytes_ipv6_addresses, other_values_to_replace)


if __name__ == "__main__":

    BYTES_MAC_ADDRESSES = convert_string_addresses_to_bytes_addresses(MAC_ADRESSES, "mac")
    BYTES_IPV4_ADDRESSES = convert_string_addresses_to_bytes_addresses(IPV4_ADDRESSES, "ipv4")
    BYTES_IPV6_ADDRESSES = convert_string_addresses_to_bytes_addresses(IPV6_ADDRESSES, "ipv6")
    BYTES_FQDN_ADDRESSES = convert_string_addresses_to_bytes_addresses(FQDN_ADDRESSES, "fqdn")

    BYTES_MAC_AND_FQDN_ADDRESSES = {**BYTES_MAC_ADDRESSES, **BYTES_FQDN_ADDRESSES}

    DIRECTORY = os.path.abspath(os.path.join(os.getcwd(), os.pardir))  # Path to 1-webrtc-leak-data

    walk_and_replace(
        DIRECTORY,
        BYTES_IPV4_ADDRESSES,
        BYTES_IPV6_ADDRESSES,
        BYTES_MAC_AND_FQDN_ADDRESSES
    )

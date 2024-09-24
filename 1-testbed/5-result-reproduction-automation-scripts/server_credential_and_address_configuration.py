#!/usr/bin/python3
# coding: utf-8
#
# Server credential and address configuration
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

"""Configuration of coturn server and VPN, SOCKS, HTTP-HTTPS proxy addresses and credentials for the experiments.

This module contains functions for configuring coturn server and VPN, SOCKS, HTTP-HTTPS proxy addresses and 
credentials to conduct the experiments
"""

__author__ = "Guillaume Nibert"
__credits__ = ["Sébastien Tixeuil", "Baptiste Polvé", "Nana J. Bakalafoua M'boussi", "Xuan Son Nguyen"]
__license__ = "GNU GPLv3"
__maintainer__ = "Guillaume Nibert"
__email__ = "guillaume.nibert@snowpack.eu"


import os


def parse_and_replace_values(filename, values_to_replace):
    """Parses a text file, replaces specified values, and saves the changes.

    Args:
        filename (str): The path to the text file to be parsed.
        values_to_replace (dict): A dictionary mapping the values to be replaced
            to their corresponding replacements.
    """

    print(filename)

    with open(filename, "r", encoding="utf8") as file:
        content = file.readlines()

    with open(filename, "w", encoding="utf8") as file:
        for line in content:
            for value, replacement in values_to_replace.items():
                line = line.replace(value, replacement)
            file.write(line)

def walk_and_replace(directory, values_to_replace):
    """Walks through a directory and recursively applies `parse_and_replace_values` to all .txt files.

    Args:
        directory (str): The path to the directory to start searching from.
        values_to_replace (dict): A dictionary mapping the values to be replaced
            to their corresponding replacements.
    """

    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".py") or filename.endswith(".js"):
                filepath = os.path.join(root, filename)
                parse_and_replace_values(filepath, values_to_replace)


if __name__ == "__main__":

    VPN_SOCKS_HTTP_HTTPS_SERVER_IPV4_ADDRESS = str(
        input("Please enter the IPv4 of your VPN, SOCKS and HTTP/HTTPS proxies: ")
    )
    VPN_SOCKS_HTTP_HTTPS_SERVER_IPV6_ADDRESS = str(
        input("Please enter the IPv6 of your VPN, SOCKS and HTTP/HTTPS proxies server: ")
    )

    COTURN_SERVER_IPV4_ADDRESS = str(input("Please enter the IPv4 of your coturn server: "))
    COTURN_SERVER_IPV6_ADDRESS = str(input("Please enter the IPv6 of your coturn server: "))
    COTURN_SERVER_USERNAME = str(input(
        "Please enter the TURN username of your coturn server (in /etc/turnserver.conf): "
    ))
    COTURN_SERVER_PASSWORD = str(input(
        "Please enter the TURN password (cleartext) of your coturn server (in /etc/turnserver.conf): "
    ))
    COTURN_SERVER_SSH_USERNAME = str(input("Please enter the SSH username of your coturn server: "))
    COTURN_SERVER_SSH_PUBKEY = str(input(
        'Please enter the SSH pubkey filename (e.g. "id_ALGORITHM") if you are on macOS, leave empty otherwhise: '
    ))
    COTURN_SERVER_SSH_PORT = str(input("Please enter the SSH port of your coturn server: "))

    VALUES_TO_REPLACE = {
        "192.0.2.1": COTURN_SERVER_IPV4_ADDRESS,
        "2001:db8::1": COTURN_SERVER_IPV6_ADDRESS,
        "TURN_USERNAME": COTURN_SERVER_USERNAME,
        "TURN_PASSWORD": COTURN_SERVER_PASSWORD,
        "coturn.anony.org": COTURN_SERVER_IPV4_ADDRESS,
        "COTURN_SSH_USERNAME": COTURN_SERVER_SSH_USERNAME,
        "COTURN_SSH_PUBKEY": COTURN_SERVER_SSH_PUBKEY if COTURN_SERVER_SSH_PUBKEY else "COTURN_SSH_PUBKEY",
        "COTURN_SSH_PORT": COTURN_SERVER_SSH_PORT,
        "198.51.100.1": VPN_SOCKS_HTTP_HTTPS_SERVER_IPV4_ADDRESS,
        "2001:db8::2": VPN_SOCKS_HTTP_HTTPS_SERVER_IPV6_ADDRESS
    }

    DIRECTORY = os.getcwd()

    walk_and_replace(f"{DIRECTORY}/1-leak-automation", VALUES_TO_REPLACE)

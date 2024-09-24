#!/usr/bin/python3
# coding: utf-8
#
# Copyright (C) 2024 Guillaume Nibert <guillaume.nibert@snowpack.eu>,
#                    Sébastien Tixeuil <sebastien.tixeuil@lip6.fr>,
#                    Baptiste Polvé <baptiste.polve@snowpack.eu>,
#                    Nana J. Bakalafoua M'boussi <nana.bakalafoua@snowpack.eu>,
#                    Xuan Son Nguyen <xuanson.nguyen@snowpack.eu>
#
# This file is part of WebRTC leak automation
#
# WebRTC leak automation is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# WebRTC leak automation is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with WebRTC leak automation. If not, see <https://www.gnu.org/licenses/>.

"""Collection of all IP addresses associated to all network interfaces

This module contains a function that automatically collect all the IP addresses associated with all the computer's
network interfaces.
"""

__author__ = "Guillaume Nibert"
__credits__ = ["Sébastien Tixeuil", "Baptiste Polvé", "Nana J. Bakalafoua M'boussi", "Xuan Son Nguyen"]
__license__ = "GNU GPLv3"
__maintainer__ = "Guillaume Nibert"
__email__ = "guillaume.nibert@snowpack.eu"

import subprocess


def get_ip_addresses_all_interfaces(operating_system: str, data_dir: str, mode_filename: str = "") -> str:
    """Run the ip addr (ipconfig on Windows) command on the WebRTC client computer and save the output in a txt file.

    Args:
        operating_system (str): accepted values in ["linux", "macos", "windows"].
        data_dir (str): ClientData directory.
        mode_filename (str, optional): if Firefox is in a container, values: 'mode1', 'mode2.2', etc. Defaults to "".

    Raises:
        ValueError: The ip addr or ipconfig cmd should return the list of all interfaces with their IP addresses.

    Returns:
        ip_addr_interfaces_stdout (str): command result on standard output.
    """

    ip_addr_interfaces_stdout = ""
    ip_addr_interfaces_command = ["ip", "addr"]
    ip_addr_interfaces_filename = ""

    if mode_filename:  # it means that the script is run in a docker container
        ip_addr_interfaces_filename = f"ip-addr-interfaces-docker-{mode_filename}"
    else:
        ip_addr_interfaces_filename = "ip-addr-interfaces-host"
        if operating_system == "windows":
            ip_addr_interfaces_command = ["ipconfig"]

    try:
        ip_a_subprocess =  subprocess.run(ip_addr_interfaces_command, capture_output=True, text=True, check=True)
        ip_addr_interfaces_stdout = ip_a_subprocess.stdout
    except subprocess.CalledProcessError as subprocess_error:
        print(f"Error running ip a (or ipconfig): {subprocess_error}")

    if not ip_addr_interfaces_stdout:
        raise ValueError('There should be ip addresses.')

    with open(f"{data_dir}/{ip_addr_interfaces_filename}.txt", mode="w+", encoding="utf8") as ip_addr_interfaces_file:
        ip_addr_interfaces_file.write(ip_addr_interfaces_stdout)

    return ip_addr_interfaces_stdout


if __name__ == "__main__":

    OPERATING_SYSTEM = "linux"

    get_ip_addresses_all_interfaces(OPERATING_SYSTEM, ".")

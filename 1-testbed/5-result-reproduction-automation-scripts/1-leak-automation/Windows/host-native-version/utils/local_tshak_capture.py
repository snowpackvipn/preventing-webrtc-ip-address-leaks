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

"""Launch a local TShark capture

This module contains a function for launching a local capture of TShark on all the computer's interfaces.
"""

__author__ = "Guillaume Nibert"
__credits__ = ["Sébastien Tixeuil", "Baptiste Polvé", "Nana J. Bakalafoua M'boussi", "Xuan Son Nguyen"]
__license__ = "GNU GPLv3"
__maintainer__ = "Guillaume Nibert"
__email__ = "guillaume.nibert@snowpack.eu"

import subprocess
import time
import signal


def launch_tshark_local_capture(host_os: str, client_data_dir: str, filename: str):
    """Run a TShark sub-process to perform local capture on port 5349 associated with the STUN/TURN protocols.

    Args:
        host_os (str): accepted values in ["linux", "macos", "windows"].
        data_dir (str): ClientData directory.
        filename (str): filename of the TShark capture.

    Returns:
        tshark_process (subprocess.Popen): TShark subpropess.
    """

    def handle_sigterm(sig, frame):
        print("Interrupting TShark capture...")
        tshark_process.send_signal(signal.SIGTERM)
    signal.signal(signal.SIGTERM, handle_sigterm)

    tshark_capture_command = ""

    if host_os == "linux":
        tshark_capture_command = [
            'tshark',
            '-ni',
            'any',
            '-f',
            "src port 5349 || dst port 5349",
            '-w',
            f"{client_data_dir}/{filename}-stun-turn.pcapng" ]
    elif host_os in ["macos", "windows"]:
        # 'tshark -ni any' option does not exist on macOS and Windows, here is a way to get it.
        tshark_view_all_interfaces_command = (
            ['tshark', '-D'] if host_os == "macos" else ['C:\\Program Files\\Wireshark\\tshark.exe', '-D']
        )
        try:
            with subprocess.Popen(tshark_view_all_interfaces_command,
                                  shell=False if host_os == "macos" else True,
                                  universal_newlines=True,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE) as tshark_view_all_interfaces_process:

                # wait for the process to terminate
                tshark_view_all_interfaces_stdout, _unused_tshark_view_all_interfaces_stderr = (
                    tshark_view_all_interfaces_process.communicate()
                )

                tshark_capture_command = (
                    ['tshark'] if host_os == "macos" else ['C:\\Program Files\\Wireshark\\tshark.exe']
                )
                excluded_interfaces = ["etwdump", "ciscodump", "randpkt", "sshdump", "udpdump", "wifidump"]
                for interface in tshark_view_all_interfaces_stdout.split('\n'):
                    if (interface
                            and not any(exluded_interface in interface for exluded_interface in excluded_interfaces)):
                        tshark_capture_command.extend(
                            ['-ni', interface.split('.')[0], '-f', 'src port 5349 || dst port 5349']
                        )
                tshark_capture_command.extend(
                    ['-w', f'{client_data_dir}/{filename}-stun-turn.pcapng']
                    if host_os == "macos"
                    else
                    ['-w', f'{client_data_dir}\\{filename}-stun-turn.pcapng']
                )
                print(tshark_capture_command)
        except subprocess.CalledProcessError as tshark_d_subprocess_called_error:
            print(f"Error running tshark -D: {tshark_d_subprocess_called_error}")

    try:
        tshark_process = subprocess.Popen(tshark_capture_command)
    except subprocess.CalledProcessError as tshark_command_called_error:
        print(f"Error running TShark: {tshark_command_called_error}")

    return tshark_process


if __name__ == "__main__":

    HOST_OS = "macos"

    TSHARK_LOCAL_CAPTURE_PROCESS = launch_tshark_local_capture(HOST_OS, ".", "test")
    time.sleep(5)
    TSHARK_LOCAL_CAPTURE_PROCESS.send_signal(signal.SIGTERM)
    TSHARK_LOCAL_CAPTURE_PROCESS.wait()

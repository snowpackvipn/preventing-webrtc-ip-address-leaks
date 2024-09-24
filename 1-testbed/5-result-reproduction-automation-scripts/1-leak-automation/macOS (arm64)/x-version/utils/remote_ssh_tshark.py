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

"""Connection to the STUN-TURN machine and gathering TShark traces.

This module contains functions for connecting via SSH to the machine hosting a STUN and TURN server and capturing &
retrieving TSharks traces.
"""

__author__ = "Guillaume Nibert"
__credits__ = ["Sébastien Tixeuil", "Baptiste Polvé", "Nana J. Bakalafoua M'boussi", "Xuan Son Nguyen"]
__license__ = "GNU GPLv3"
__maintainer__ = "Guillaume Nibert"
__email__ = "guillaume.nibert@snowpack.eu"

import os
import signal
import subprocess

import paramiko
from paramiko.common import cMSG_CHANNEL_REQUEST


def tshark_remote_ssh_client(host_os: str):
    """Create a SSH connection to the STUN-TURN server.

    Returns:
        ssh_client (paramiko.SSHClient): SSH connection to the STUN-TURN server.
    """

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    if host_os == "macos":
        ssh_client.connect(
            hostname="coturn.anony.org",
            port="COTURN_SSH_PORT",
            username="COTURN_SSH_USERNAME",
            key_filename=f"{os.path.expanduser('~/.ssh')}/COTURN_SSH_PUBKEY"
        )
    else:
        ssh_client.connect(
            hostname="coturn.anony.org",
            port="COTURN_SSH_PORT",
            username="COTURN_SSH_USERNAME"
        )

    return ssh_client


def create_sigterm_paramiko_ssh_message(channel):
    """Creates a SIGTERM signal via paramiko to stop remote TShark capture.

    Args:
        channel (paramiko.Channel): paramiko stdin channel associated with the executed tshark command.

    Returns:
        message (paramiko.Message): paramiko.Message that contains the SIGTERM signal.
    """

    message = paramiko.Message()
    message.add_byte(cMSG_CHANNEL_REQUEST)
    message.add_int(channel.remote_chanid)
    message.add_string("signal")
    message.add_boolean(False)
    message.add_string(signal.Signals.SIGTERM.name[3:])

    return message


def gather_remote_tshark_traces(host_os: str, data_dir: str) -> str:
    """Run the rsync command on the WebRTC client computer to gather the TShark pcapng traces from the STUN/TURN server.

    Args:
        host_os (str): accepted values in ["linux", "macos", "windows"].
        data_dir (str): STUN-TURN-ServerData directory.
    """

    gather_command = ""

    print(data_dir)

    if host_os == "windows":
        gather_command = [
            "scp",
            "-P",
            "COTURN_SSH_PORT",
            f"COTURN_SSH_USERNAME@coturn.anony.org:~/tshark_traces_{host_os}/*",
            f"{data_dir}"
        ]
    elif host_os in ("linux", "macos"):
        gather_command = [
            "rsync",
            "-rvz",
            "--progress",
            "-e",
            "ssh -p COTURN_SSH_PORT",
            f"COTURN_SSH_USERNAME@coturn.anony.org:~/tshark_traces_{host_os}/*",
            f"{data_dir}"
        ]

    try:
        gather_subprocess =  subprocess.run(gather_command, capture_output=True, text=True, check=True)
        gather_stdout = gather_subprocess.stdout
        print(gather_stdout)
    except subprocess.CalledProcessError as gather_ice_candidates_subprocess_error:
        print(f"Error running command: {gather_ice_candidates_subprocess_error}")


if __name__ == "__main__":

    HOST_OS = "linux"

    # TShark STUN-TURN server remote capture for each WebRTC handling mode
    TSHARK_REMOTE_COMMAND = (
        f'tshark -ni wlan0 -f "src port 5349 || dst port 5349" -w '
        f'/home/COTURN_SSH_USERNAME/tshark_traces_{HOST_OS}/test_remote.pcapng'
    )

    print(f"\nTShark remote command: {TSHARK_REMOTE_COMMAND}\n")

    TSHARK_REMOTE_CAPTURE_SSH_CLIENT = tshark_remote_ssh_client(HOST_OS)
    TSHARK_REMOTE_CAPTURE_STDIN, TSHARK_REMOTE_CAPTURE_STDOUT, _ = (
        TSHARK_REMOTE_CAPTURE_SSH_CLIENT.exec_command(TSHARK_REMOTE_COMMAND, get_pty=True)
    )
    TSHARK_REMOTE_CAPTURE_STDIN_CHANNEL = TSHARK_REMOTE_CAPTURE_STDIN.channel

    FIRST_LINE_TSHARK_REMOTE_CAPTURE_STDOUT = next(iter(TSHARK_REMOTE_CAPTURE_STDOUT.readline, ""))

    if FIRST_LINE_TSHARK_REMOTE_CAPTURE_STDOUT[:20] == "Capturing on 'wlan0'":
        # Terminate the STUN-TURN remote TShark capture.
        SIGTERM_MESSAGE = create_sigterm_paramiko_ssh_message(TSHARK_REMOTE_CAPTURE_STDIN_CHANNEL)

        # _send_user_message is private API
        # pylint: disable=protected-access
        TSHARK_REMOTE_CAPTURE_STDIN_CHANNEL.transport._send_user_message(SIGTERM_MESSAGE)

        # Terminate the STUN-TURN SSH connection.
        TSHARK_REMOTE_CAPTURE_SSH_CLIENT.close()

    else:
        print("Error starting REMOTE TShark captures.")


    # Gather STUN-TURN remote TShark traces
    gather_remote_tshark_traces(HOST_OS, ".")

    # Remove STUN-TURN remote TShark traces
    REMOVE_TSHARK_TRACES_REMOTE_COMMAND = f'rm -rf tshark_traces_{HOST_OS}/ && mkdir tshark_traces_{HOST_OS}'
    REMOTE_STUNTURN_TSHARK_SSH_CLIENT = tshark_remote_ssh_client(HOST_OS)
    REMOTE_STUNTURN_TSHARK_SSH_CLIENT.exec_command(REMOVE_TSHARK_TRACES_REMOTE_COMMAND)
    REMOTE_STUNTURN_TSHARK_SSH_CLIENT.close()

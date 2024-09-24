#!/usr/bin/python3
# coding: utf-8
#
# WebRTC leak automation
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

__author__ = "Guillaume Nibert"
__credits__ = ["Sébastien Tixeuil", "Baptiste Polvé", "Nana J. Bakalafoua M'boussi", "Xuan Son Nguyen"]
__license__ = "GNU GPLv3"
__maintainer__ = "Guillaume Nibert"
__email__ = "guillaume.nibert@snowpack.eu"

import os
import subprocess
import signal
import time

from constants import PLATFORMS, LEAK_STUDIES, WEB_BROWSERS
from constants import IP_VERSIONS, WEBRTC_HANDLING_MODES, USER_CONSENTS, PROXIES
from constants import ICE_CANDIDATES_TXT_DEFAULT_CONF_HEADING, ICE_CANDIDATES_TXT_FORCED_CONF_HEADING

from utils.script_parser import script_arguments
from utils.script_parser import validate_arguments

from utils.ip_addr import get_ip_addresses_all_interfaces

from utils.local_tshak_capture import launch_tshark_local_capture

from utils.remote_ssh_tshark import tshark_remote_ssh_client
from utils.remote_ssh_tshark import create_sigterm_paramiko_ssh_message
from utils.remote_ssh_tshark import gather_remote_tshark_traces

from utils.storage_init import data_dirs, initialise_leak_data_storage

from utils.call_docker_compose import get_docker_compose_leak_commands_and_env

from leak import run_leak, webdriver_service

DEBUG = False


if __name__ == "__main__":

    args = script_arguments("WebRTC gather ICE candidates").parse_args()
    validate_arguments(args)

    if DEBUG:
        print(
            f"Host platform: {args.host_platform}\n"
            f"Linux host window manager: {args.linux_host_window_manager}\n"
            f"Native web browser tested: {args.web_browser}\n"
            f"Wanted proxy's type: {args.proxy}\n"
            f"IP version: {args.ip}\n"
            f"Wanted study: {args.study}\n"
            f"Web browser containerised: {args.containerised_firefox}\n"
            f"Container window manager: {args.container_window_manager}\n"
            f"WebRTC IP handling policy: {args.mode}\n"
            f"getUserMedia() consent: {args.user_consent}"
        )

    leaks_study_folder_name = LEAK_STUDIES.get(args.study)
    web_browser_full_name = WEB_BROWSERS.get(args.web_browser)

    webrtc_ip_handling_policies = ["default"] if args.web_browser == "safari" else WEBRTC_HANDLING_MODES.get(args.study)

    proxy_name = PROXIES.get(args.proxy, {}).get("name", "")
    ip_version = IP_VERSIONS.get(args.ip, "")

    configuration_folder_name = (
        PLATFORMS.get(f"{args.host_platform}-{args.linux_host_window_manager}")
        if args.host_platform == "linux"
        else
        PLATFORMS.get(f"{args.host_platform}")
    )

    client_data_dir, stun_turn_server_data_dir = data_dirs(args.host_platform,
                                                           configuration_folder_name,
                                                           leaks_study_folder_name,
                                                           web_browser_full_name,
                                                           args.containerised_firefox,
                                                           args.container_window_manager,
                                                           proxy_name,
                                                           ip_version)

    if DEBUG:
        print(
            f"client_data_dir: {client_data_dir}\n"
            f"stun_turn_server_data_dir: {stun_turn_server_data_dir}"
        )

    os.makedirs(client_data_dir, exist_ok=True)

    # 1. Create a dict for storing the ICE candidates extracted from the SDP offers, the filenames of the TShark traces
    #    and the headings associated with the ice-candidates.txt file.
    leak_data_storage = initialise_leak_data_storage(webrtc_ip_handling_policies, USER_CONSENTS, args.web_browser)

    webdriver_service = webdriver_service(args.web_browser, args.host_platform, args.containerised_firefox)

    # If this script is run in a docker container
    if args.mode and args.user_consent in (False, True):

        # 2. Store the list of the DOCKER WebRTC client network interfaces in a file called
        # ip-addr-interfaces-docker-mode-X-UC/NUC.txt
        client_ip_addresses_interfaces = get_ip_addresses_all_interfaces(
            args.host_platform,
            client_data_dir,
            leak_data_storage[args.mode][args.user_consent]["raw_data_filename"]
        )

        leak_data_storage[args.mode][args.user_consent]["ice-candidates"] = run_leak(
            args.web_browser,
            webdriver_service,
            args.user_consent,
            args.mode,
            args.host_platform,
            args.containerised_firefox,
            args.proxy,
            args.ip
        )


        # Write the list of ICE candidates in the ice-candidates.txt file for each WebRTC handling mode.
        mode_filename = leak_data_storage[args.mode][args.user_consent]["raw_data_filename"]
        print(mode_filename)

        with open(f"{client_data_dir}/ice-candidates-{mode_filename}-stun-turn.txt",
                  "w",
                  encoding="utf8") as ice_candidates_txt:
            ice_candidates_txt.write(
                leak_data_storage[args.mode][args.user_consent]["configuration_heading"] + "\n\n"
            )
            ice_candidates_txt.write(
                "\n".join(leak_data_storage[args.mode][args.user_consent]["ice-candidates"]) + "\n\n"
            )

    elif args.mode is None and args.user_consent is None:
        # Make sure that the tshark_trace folder is empty
        remove_tshark_traces_remote_command = (
            f'rm -rf tshark_traces_{args.host_platform}/ && mkdir tshark_traces_{args.host_platform}'
        )
        remote_stunturn_tshark_ssh_client = tshark_remote_ssh_client(args.host_platform)
        remote_stunturn_tshark_ssh_client.exec_command(remove_tshark_traces_remote_command)
        remote_stunturn_tshark_ssh_client.close()

        os.makedirs(stun_turn_server_data_dir, exist_ok=True)

        # 2. Store the list of the HOST WebRTC client network interfaces in a file called ip-addr-interfaces-host.txt
        client_ip_addresses_interfaces = get_ip_addresses_all_interfaces(args.host_platform, client_data_dir)

        # 3. Gather ICE candidates and collect WebRTC client and STUN-TURN server TShark traces.
        for webrtc_handling_mode in webrtc_ip_handling_policies:
            for user_consent in USER_CONSENTS:

                tshark_trace_filename = leak_data_storage[webrtc_handling_mode][user_consent]["raw_data_filename"]

                # TShark STUN-TURN server remote capture for each WebRTC handling mode
                tshark_remote_command = (
                    f'tshark -ni wlan0 -f "src port 5349 || dst port 5349" -w '
                    f'/home/COTURN_SSH_USERNAME/tshark_traces_{args.host_platform}/{tshark_trace_filename}-stun-turn.pcapng'
                )

                print(f"\nTShark remote command: {tshark_remote_command}\n")

                tshark_remote_capture_ssh_client = tshark_remote_ssh_client(args.host_platform)
                tshark_remote_capture_stdin, tshark_remote_capture_stdout, _ = (
                    tshark_remote_capture_ssh_client.exec_command(tshark_remote_command, get_pty=True)
                )
                tshark_remote_capture_stdin_channel = tshark_remote_capture_stdin.channel

                first_line_tshark_remote_capture_stdout = next(iter(tshark_remote_capture_stdout.readline, ""))

                # TShark WebRTC client local capture for each WebRTC handling mode
                tshark_local_capture_process = launch_tshark_local_capture(
                    args.host_platform, client_data_dir, tshark_trace_filename
                )

                if (tshark_local_capture_process
                    and first_line_tshark_remote_capture_stdout[:20] == "Capturing on 'wlan0'"):

                    time.sleep(2)  # Wait for the local tshak command initialisation

                    if args.containerised_firefox:

                        (shell_env,
                            docker_compose_leak_up_cmd,
                            docker_compose_leak_down_cmd) = get_docker_compose_leak_commands_and_env(
                            args.host_platform,
                            args.study,
                            webrtc_handling_mode,
                            user_consent,
                            args.container_window_manager,
                            args.proxy,
                            args.ip
                        )

                        with subprocess.Popen(docker_compose_leak_up_cmd,
                                              env=shell_env) as docker_compose_leak_up_process:
                            docker_compose_leak_up_process.wait()

                        with subprocess.Popen(docker_compose_leak_down_cmd,
                                              env=shell_env) as docker_compose_leak_down_process:
                            docker_compose_leak_down_process.wait()

                    else:
                        leak_data_storage[webrtc_handling_mode][user_consent]["ice-candidates"] = run_leak(
                            args.web_browser,
                            webdriver_service,
                            user_consent,
                            webrtc_handling_mode,
                            args.host_platform,
                            args.containerised_firefox,
                            args.proxy,
                            args.ip
                        )

                    # Terminate the STUN-TURN remote TShark capture.
                    sigterm_message = create_sigterm_paramiko_ssh_message(tshark_remote_capture_stdin_channel)

                    # _send_user_message is private API
                    # pylint: disable=protected-access
                    tshark_remote_capture_stdin_channel.transport._send_user_message(sigterm_message)

                    # Terminate the WebRTC client local TShark capture.
                    tshark_local_capture_process.send_signal(signal.SIGTERM)

                    # Terminate the STUN-TURN SSH connection and wait for the local TShark capture termination.
                    tshark_remote_capture_stdin.close()
                    tshark_remote_capture_ssh_client.close()
                    tshark_local_capture_process.wait()

                else:
                    print("Error starting LOCAL and/or REMOTE TShark captures.")

        # Gather STUN-TURN remote TShark traces
        gather_remote_tshark_traces(args.host_platform, stun_turn_server_data_dir)

        # Remove STUN-TURN remote TShark traces
        remove_tshark_traces_remote_command = (
            f'rm -rf tshark_traces_{args.host_platform}/ && mkdir tshark_traces_{args.host_platform}'
        )
        remote_stunturn_tshark_ssh_client = tshark_remote_ssh_client(args.host_platform)
        remote_stunturn_tshark_ssh_client.exec_command(remove_tshark_traces_remote_command)
        remote_stunturn_tshark_ssh_client.close()

        if args.containerised_firefox:
            # Write the list of ICE candidates in the ice-candidates.txt file for each WebRTC handling mode.
            with open(f"{client_data_dir}/ice-candidates.txt", "w", encoding="utf8") as ice_candidates_txt:
                ice_candidates_txt.write(ICE_CANDIDATES_TXT_DEFAULT_CONF_HEADING + "\n\n")

                for webrtc_handling_mode in webrtc_ip_handling_policies:
                    if webrtc_handling_mode == "forced_mode_2":
                        ice_candidates_txt.write(ICE_CANDIDATES_TXT_FORCED_CONF_HEADING + "\n\n")
                    for user_consent in USER_CONSENTS:
                        mode_filename = leak_data_storage[webrtc_handling_mode][user_consent]["raw_data_filename"]

                        with open(f"{client_data_dir}/ice-candidates-{mode_filename}-stun-turn.txt",
                                  "r",
                                  encoding="utf8") as ice_candidates_per_mode_dockerised:
                            all_text = ice_candidates_per_mode_dockerised.readlines()

                            ice_candidates_txt.writelines(all_text)
                            ice_candidates_txt.write("\n")

                        os.remove(f"{client_data_dir}/ice-candidates-{mode_filename}-stun-turn.txt")

        else:
            # Write the list of ICE candidates in the ice-candidates.txt file for each WebRTC handling mode.
            with open(f"{client_data_dir}/ice-candidates.txt", "w", encoding="utf8") as ice_candidates_txt:
                ice_candidates_txt.write(ICE_CANDIDATES_TXT_DEFAULT_CONF_HEADING + "\n\n")

                for webrtc_handling_mode in webrtc_ip_handling_policies:
                    if webrtc_handling_mode == "forced_mode_2":
                        ice_candidates_txt.write(ICE_CANDIDATES_TXT_FORCED_CONF_HEADING + "\n\n")
                    for user_consent in USER_CONSENTS:
                        ice_candidates_txt.write(
                            leak_data_storage[webrtc_handling_mode][user_consent]["configuration_heading"] + "\n\n"
                        )
                        ice_candidates_txt.write(
                            "\n".join(leak_data_storage[webrtc_handling_mode][user_consent]["ice-candidates"]) + "\n\n"
                        )

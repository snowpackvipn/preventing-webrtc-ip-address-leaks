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

"""Creation of data storage locations.

This module contains functions for creating data storage locations.
"""

__author__ = "Guillaume Nibert"
__credits__ = ["Sébastien Tixeuil", "Baptiste Polvé", "Nana J. Bakalafoua M'boussi", "Xuan Son Nguyen"]
__license__ = "GNU GPLv3"
__maintainer__ = "Guillaume Nibert"
__email__ = "guillaume.nibert@snowpack.eu"

import os


def data_dirs(host_os: str,
              configuration_folder_name: str,
              leaks_study_folder_name: str,
              web_browser_full_name: str,
              containerised_firefox: bool,
              container_window_manager: str | None,
              proxy_name: str = "",
              ip_version: int = 0) -> tuple:
    """Creation of the folders containing the raw data and TShark traces associated with the different configurations
       studied.

    Args:
        host_os (str): accepted values in ["linux", "macos", "windows"]
        configuration_folder_name (str): host platform configuration (e.g. "Linux (Ubuntu) - Wayland" or "Windows")
        leaks_study_folder_name (str): from constants.py, LEAK_STUDIES[chosen_study] = "1 - Leaks in popular nativel..."
        web_browser_full_name (str): "Mozilla Firefox", "Google Chrome", "Microsoft Edge", "Opera" or "Brave"
        containerised_firefox (bool): 'True' if Firefox is containerised else 'False'.
        container_window_manager (str | None): 'x', 'wayland' or None.
        proxy_name (str, optional): from constants.py, PROXIES[chosen_proxy]["name"] = e.g. "WireGuard". Defaults to "".
        ip_version (str, optional): from constants.py, IP_VERSIONS[chosen_ipversion] = e.g. "IPv4". Defaults to "".

    Raises:
        ValueError: ClientData and STUN-TURN-ServerData dirs must have been created after the function was executed.

    Returns:
        tuple: client_data_dir (str): ---> ip-addr-interfaces.txt; ice-candidates.txt; modes.pcapng,
               stun_turn_server_data_dir (str): ---> modes.pcapng
    """

    home = os.path.expanduser("~")
    base_dir = f"{home}/Downloads/1-webrtc-leak-data/{configuration_folder_name}/{leaks_study_folder_name}"
    client_data_dir = ""
    stun_turn_server_data_dir = ""

    if not containerised_firefox:
        if not proxy_name and not ip_version:
            client_data_dir = f"{base_dir}/{web_browser_full_name}/ClientData"
            stun_turn_server_data_dir = f"{base_dir}/{web_browser_full_name}/STUN-TURN-ServerData"
        else:
            client_data_dir = f"{base_dir}/{web_browser_full_name} + {proxy_name} ({ip_version} tunnel)/ClientData"
            stun_turn_server_data_dir = (
                f"{base_dir}/"
                f"{web_browser_full_name} + {proxy_name} ({ip_version} tunnel)/"
                f"STUN-TURN-ServerData"
            )

    else:
        if host_os == "windows" and container_window_manager is not None:
            if not proxy_name and not ip_version:
                client_data_dir = f"{base_dir}/{web_browser_full_name} dockerised {container_window_manager}/ClientData"
                stun_turn_server_data_dir = (
                    f"{base_dir}/{web_browser_full_name} dockerised {container_window_manager}/STUN-TURN-ServerData"
                )
            else:
                client_data_dir = (
                    f"{base_dir}/"
                    f"{web_browser_full_name} dockerised {container_window_manager} "
                    f"+ {proxy_name} ({ip_version} tunnel)/"
                    f"ClientData"
                )
                stun_turn_server_data_dir = (
                    f"{base_dir}/"
                    f"{web_browser_full_name} dockerised {container_window_manager} "
                    f"+ {proxy_name} ({ip_version} tunnel)/"
                    f"STUN-TURN-ServerData"
                )
        elif host_os in ["linux", "macos"]:
            if not proxy_name and not ip_version:
                client_data_dir = f"{base_dir}/{web_browser_full_name} dockerised/ClientData"
                stun_turn_server_data_dir = f"{base_dir}/{web_browser_full_name} dockerised/STUN-TURN-ServerData"
            else:
                client_data_dir = (
                    f"{base_dir}/"
                    f"{web_browser_full_name} dockerised + {proxy_name} ({ip_version} tunnel)/"
                    f"ClientData"
                )
                stun_turn_server_data_dir = (
                    f"{base_dir}/"
                    f"{web_browser_full_name} dockerised + {proxy_name} ({ip_version} tunnel)/"
                    f"STUN-TURN-ServerData"
                )

    if not base_dir or not client_data_dir or not stun_turn_server_data_dir:
        raise ValueError("Data directories not well defined.")

    return(client_data_dir, stun_turn_server_data_dir)


def initialise_leak_data_storage(webrtc_handling_modes: list, user_consents: list, web_browser: str) -> dict:
    """Initialise a dictionary which will store the results, the filenames of the TShark traces (ice-candidates-mode...
    for the containerised Firefox leak test) and the headings associated with the ice-candidates.txt file.

    Args:
        webrtc_handling_modes (list): from constants.py, WEBRTC_HANDLING_MODES = ["default", "forced_mode_2"...].
        user_consents (list): from constants.py, USER_CONSENTS = [True, False].
        web_browser (str): accepted values in ["firefox", "chrome", "edge", "safari", "opera", "brave"].

    Returns:
        leak_data_storage (dict): dictionary which stores the results, the filenames of the TShark traces and the
                                  headings associated with the ice-candidates.txt file.
    """

    leak_data_storage = {}

    for webrtc_handling_mode in webrtc_handling_modes:
        leak_data_storage[webrtc_handling_mode] = {}
        for user_consent in user_consents:
            leak_data_storage[webrtc_handling_mode][user_consent] = {}
            if webrtc_handling_mode == "default" and user_consent:
                if web_browser != "safari":
                    leak_data_storage[webrtc_handling_mode][user_consent]["configuration_heading"] = "Mode 1 - User consent"
                    leak_data_storage[webrtc_handling_mode][user_consent]["raw_data_filename"] = "default-mode1"
                else:
                    leak_data_storage[webrtc_handling_mode][user_consent]["configuration_heading"] = (
                        "Mode 2 - User consent"
                    )
                    leak_data_storage[webrtc_handling_mode][user_consent]["raw_data_filename"] = "default-mode2-UC"
            elif webrtc_handling_mode == "default" and not user_consent:
                if web_browser != "safari":
                    leak_data_storage[webrtc_handling_mode][user_consent]["configuration_heading"] = (
                        "Mode 2.2 - No user consent"
                    )
                    leak_data_storage[webrtc_handling_mode][user_consent]["raw_data_filename"] = "default-mode2.2"
                else:
                    leak_data_storage[webrtc_handling_mode][user_consent]["configuration_heading"] = (
                        "Mode 2 - No user consent"
                    )
                    leak_data_storage[webrtc_handling_mode][user_consent]["raw_data_filename"] = "default-mode2-NUC"
            elif webrtc_handling_mode == "forced_mode_2" and user_consent:
                leak_data_storage[webrtc_handling_mode][user_consent]["configuration_heading"] = (
                    "Mode 2 - User consent"
                )
                leak_data_storage[webrtc_handling_mode][user_consent]["raw_data_filename"] = "forced-mode2-UC"
            elif webrtc_handling_mode == "forced_mode_2" and not user_consent:
                if web_browser != "firefox":
                    leak_data_storage[webrtc_handling_mode][user_consent]["configuration_heading"] = (
                        "Mode 2 - No user consent"
                    )
                    leak_data_storage[webrtc_handling_mode][user_consent]["raw_data_filename"] = "forced-mode2-NUC"
                else:
                    leak_data_storage[webrtc_handling_mode][user_consent]["configuration_heading"] = (
                        "Mode 2 -> 2.2 - No user consent"
                    )
                    leak_data_storage[webrtc_handling_mode][user_consent]["raw_data_filename"] = "forced-mode2-2.2-NUC"
            elif webrtc_handling_mode == "forced_mode_3" and user_consent:
                leak_data_storage[webrtc_handling_mode][user_consent]["configuration_heading"] = "Mode 3 - User consent"
                leak_data_storage[webrtc_handling_mode][user_consent]["raw_data_filename"] = "forced-mode3-UC"
            elif webrtc_handling_mode == "forced_mode_3" and not user_consent:
                leak_data_storage[webrtc_handling_mode][user_consent]["configuration_heading"] = (
                    "Mode 3 - No user consent"
                )
                leak_data_storage[webrtc_handling_mode][user_consent]["raw_data_filename"] = "forced-mode3-NUC"
            elif webrtc_handling_mode == "forced_mode_4" and user_consent:
                leak_data_storage[webrtc_handling_mode][user_consent]["configuration_heading"] = "Mode 4 - User consent"
                leak_data_storage[webrtc_handling_mode][user_consent]["raw_data_filename"] = "forced-mode4-UC"
            elif webrtc_handling_mode == "forced_mode_4" and not user_consent:
                leak_data_storage[webrtc_handling_mode][user_consent]["configuration_heading"] = (
                    "Mode 4 - No user consent"
                )
                leak_data_storage[webrtc_handling_mode][user_consent]["raw_data_filename"] = "forced-mode4-NUC"
            elif webrtc_handling_mode == "compromised" and user_consent:
                leak_data_storage[webrtc_handling_mode][user_consent]["configuration_heading"] = (
                    "Compromised - User consent"
                )
                leak_data_storage[webrtc_handling_mode][user_consent]["raw_data_filename"] = "compromised-UC"
            elif webrtc_handling_mode == "compromised" and not user_consent:
                leak_data_storage[webrtc_handling_mode][user_consent]["configuration_heading"] = (
                    "Compromised - No user consent"
                )
                leak_data_storage[webrtc_handling_mode][user_consent]["raw_data_filename"] = "compromised-NUC"


    return leak_data_storage


if __name__ == "__main__":

    HOST_OS = "linux"
    CONFIGURATION_FOLDER_NAME = "Linux (Ubuntu) - Wayland"
    LEAK_STUDY_FOLDER_NAME = "1 - Leaks in popular natively executed web browsers"
    WEB_BROWSER = "firefox"
    WEB_BROWSER_FULL_NAME = "Mozilla Firefox"
    CONTAINERISED_FIREFOX = True
    CONTAINER_WINDOW_MANAGER = "wayland"
    PROXY_NAME = "OpenVPN UDP"
    IP_VERSION = "IPv6"

    WEBRTC_HANDLING_MODES = ("default", "forced_mode_2", "forced_mode_3", "forced_mode_4")
    USER_CONSENTS = (True, False)

    CLIENT_DATA_DIR, STUN_TURN_SERVER_DATA_DIR = data_dirs(HOST_OS,
                                                           CONFIGURATION_FOLDER_NAME,
                                                           LEAK_STUDY_FOLDER_NAME,
                                                           WEB_BROWSER_FULL_NAME,
                                                           CONTAINERISED_FIREFOX,
                                                           CONTAINER_WINDOW_MANAGER,
                                                           PROXY_NAME,
                                                           IP_VERSION)

    LEAK_DATA_STORAGE = initialise_leak_data_storage(WEBRTC_HANDLING_MODES, USER_CONSENTS, WEB_BROWSER)

    print(
        f"ClientData dir: {CLIENT_DATA_DIR}\n",
        f"STUN-TURN-ServerData dir: {STUN_TURN_SERVER_DATA_DIR}\n\n"
        f"leak_data_storage = {LEAK_DATA_STORAGE}"
    )

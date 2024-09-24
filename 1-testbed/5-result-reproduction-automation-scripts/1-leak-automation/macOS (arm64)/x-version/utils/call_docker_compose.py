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

"""Creation of the subprocess commands that will be executed to perform the Firefox WebRTC leak in a docker container.

This module contains a function that automatically create the docker compose subprocess commands that will be executed
to perform the Firefox WebRTC leak in a docker container. It will also return the environment variable needed for macOS
and Linux.
"""

__author__ = "Guillaume Nibert"
__credits__ = ["Sébastien Tixeuil", "Baptiste Polvé", "Nana J. Bakalafoua M'boussi", "Xuan Son Nguyen"]
__license__ = "GNU GPLv3"
__maintainer__ = "Guillaume Nibert"
__email__ = "guillaume.nibert@snowpack.eu"

import os
if os.name == "posix":
    import grp


def get_docker_compose_leak_commands_and_env(host_os: str,
                                             study: str,
                                             webrtc_behaviour: str,
                                             get_user_media_consent: bool,
                                             container_window_manager: str,
                                             proxy_protocol: str = "",
                                             proxy_network_version: int = 0,
                                             docker_compose_base_path: str = ".") -> tuple:
    """Create the subprocess commands that will be executed to perform the Firefox WebRTC leak in a docker container.

    Args:
        host_os (str): accepted values in ["linux", "macos", "windows"].
        study (str): from constants.py, LEAK_STUDIES[chosen_study] = "1 - Leaks in popular nativel..."
        webrtc_behaviour (str): ["vanilla", "forced_mode_2", "forced_mode_3", "forced_mode_4" or "compromised"]
        get_user_media_consent (bool): getUserMedia() consent, 'True' or 'False'.
        container_window_manager (str): accepted values in ["x", "wayland"]
        proxy_protocol (str, optional): ["socks", "http-https", "openvpn" or "wireguard"]. Defaults to "".
        proxy_network_version (str, optional): accepted values in [4, 6]. Defaults to "".
        docker_compose_base_path (str, optional): for test purposes. Default to ".".

    Raises:
        ValueError: if Docker Desktop for macOS and Windows is associated with IPv6, if docker is used with wayland on
                    macOS or if the entrypoint is still empty at the end of the run of this function.

    Returns:
        tuple: environment variables (dict), docker up command (list), docker down command (list).
    """

    shell_env = os.environ.copy()
    docker_compose_entry_point = ""
    docker_compose_camera_device = (
        "        devices:\n"
        "            -  /dev/video0:/dev/video0\n"
    )
    docker_compose_remove_camera_device = (
        "        # devices:\n"
        "            # -  /dev/video0:/dev/video0\n"
    )

    if host_os == "linux":

        uid, gid, render_gid = str(os.getuid()), str(os.getgid()), str(grp.getgrnam('render').gr_gid)

        shell_env["UID"] = uid
        shell_env["GID"] = gid
        shell_env["RENDER_GID"] = render_gid

        docker_compose_entry_point = (
            f"        entrypoint: "
            f"\"python3 ./main.py --host-platform {host_os} "
            f"--linux-host-window-manager {container_window_manager} "
            f"--web-browser firefox "
            f"--study {study} "
            f"--web-browser-containerised "
            f"--container-window-manager {container_window_manager} "
            f"--mode {webrtc_behaviour} "
            f"--user-consent {get_user_media_consent}\"\n"
        )
        if proxy_protocol and proxy_network_version:
            docker_compose_entry_point = (
                f"        entrypoint: "
                f"\"python3 ./main.py --host-platform {host_os} "
                f"--linux-host-window-manager {container_window_manager} "
                f"--web-browser firefox "
                f"--study {study} "
                f"--proxy {proxy_protocol} "
                f"--ip {proxy_network_version} "
                f"--web-browser-containerised "
                f"--container-window-manager {container_window_manager} "
                f"--mode {webrtc_behaviour} "
                f"--user-consent {get_user_media_consent}\"\n"
            )
    elif host_os in ("macos", "windows"):
        if proxy_network_version == 6:
            raise ValueError("Docker Desktop for Windows and macOS does not support IPv6.")
        if host_os == "macos":
            if container_window_manager == "wayland":
                raise ValueError("There is no wayland compositor on macOS.")

            uid, gid = str(os.getuid()), str(os.getgid())

            shell_env["UID"] = uid
            shell_env["GID"] = gid

        docker_compose_entry_point = (
            f"        entrypoint: "
            f"\"python3 ./main.py --host-platform {host_os} "
            f"--web-browser firefox "
            f"--study {study} "
            f"--web-browser-containerised "
            f"--container-window-manager {container_window_manager} "
            f"--mode {webrtc_behaviour} "
            f"--user-consent {get_user_media_consent}\"\n"
        )
        if proxy_protocol and proxy_network_version:
            docker_compose_entry_point = (
                f"        entrypoint: "
                f"\"python3 ./main.py --host-platform {host_os} "
                f"--web-browser firefox "
                f"--study {study} "
                f"--proxy {proxy_protocol} "
                f"--ip {proxy_network_version} "
                f"--web-browser-containerised "
                f"--container-window-manager {container_window_manager} "
                f"--mode {webrtc_behaviour} "
                f"--user-consent {get_user_media_consent}\"\n"
            )

    if not docker_compose_entry_point:
        raise ValueError("The docker compose entrypoint must be set.")

    with (
        open(f"{docker_compose_base_path}/docker-compose-firefox-{container_window_manager}-{host_os}-automated-leaks"
              ".yml", "r", encoding="utf8") as docker_compose_yml_old,
        open(f"{docker_compose_base_path}/docker-compose-firefox-{container_window_manager}-{host_os}-automated-leaks"
              "-new.yml", "w", encoding="utf8") as docker_compose_yml_new
              ):
        for line in docker_compose_yml_old:
            if "entrypoint" in line:
                docker_compose_yml_new.write(docker_compose_entry_point)
            else:
                if host_os == "windows" and proxy_protocol == "wireguard":
                    if "        devices:\n" in line:
                        docker_compose_yml_new.write("        # devices:\n")
                    elif "            -  /dev/video0:/dev/video0\n" in line:
                        docker_compose_yml_new.write("            # -  /dev/video0:/dev/video0\n")
                    else:
                        docker_compose_yml_new.write(line)
                else:
                    if "        # devices:\n" in line:
                        docker_compose_yml_new.write("        devices:\n")
                    elif "            # -  /dev/video0:/dev/video0\n" in line:
                        docker_compose_yml_new.write("            -  /dev/video0:/dev/video0\n")
                    else:
                        docker_compose_yml_new.write(line)
                

    os.remove(f"./docker-compose-firefox-{container_window_manager}-{host_os}-automated-leaks"
               ".yml")
    os.rename(f"./docker-compose-firefox-{container_window_manager}-{host_os}-automated-leaks"
               "-new.yml",
              f"./docker-compose-firefox-{container_window_manager}-{host_os}-automated-leaks"
               ".yml")

    docker_compose_up_command = [
        "docker",
        "compose",
        "-f",
        f"./docker-compose-firefox-{container_window_manager}-{host_os}-automated-leaks.yml",
        "up"
    ]

    docker_compose_down_command = [
        "docker",
        "compose",
        "-f",
        f"./docker-compose-firefox-{container_window_manager}-{host_os}-automated-leaks.yml",
        "down"
    ]

    return (shell_env, docker_compose_up_command, docker_compose_down_command)


if __name__ == "__main__":

    HOST_OS = "windows"
    STUDY = "1 - Leaks in popular natively executed web browsers"
    WEBRTC_BEHAVIOUR = "forced_mode_2"
    GET_USER_MEDIA_CONSENT = True
    CONTAINERISED_WINDOW_MANAGER = "wayland"
    PROXY_PROTOCOL = "wireguard"
    PROXY_NETWORK_VERSION = 4

    SHELL_ENV, DOCKER_COMPOSE_UP_CMD, DOCKER_COMPOSE_DOWN_CMD = get_docker_compose_leak_commands_and_env(
        HOST_OS,
        STUDY,
        WEBRTC_BEHAVIOUR,
        GET_USER_MEDIA_CONSENT,
        CONTAINERISED_WINDOW_MANAGER,
        PROXY_PROTOCOL,
        PROXY_NETWORK_VERSION
    )

    print(
        f"SHELL_ENV = {SHELL_ENV}\n\n"
        f"DOCKER_COMPOSE_UP_CMD = {DOCKER_COMPOSE_UP_CMD}\n\n"
        f"DOCKER_COMPOSE_DOWN_CMD = {DOCKER_COMPOSE_DOWN_CMD}"
    )

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

"""Add arguments to the main script

This module contains functions for adding and validating arguments to the main script.
"""

__author__ = "Guillaume Nibert"
__credits__ = ["Sébastien Tixeuil", "Baptiste Polvé", "Nana J. Bakalafoua M'boussi", "Xuan Son Nguyen"]
__license__ = "GNU GPLv3"
__maintainer__ = "Guillaume Nibert"
__email__ = "guillaume.nibert@snowpack.eu"

import argparse


def user_consent_argument(value: str | None):
    """Function that transforms a True (resp. False) string argument into a True (resp. False) Boolean.

    Args:
        value (str | None): values in all forms of the words true/false (True, true, TrUe, FAlse, etc.) and None.

    Raises:
        argparse.ArgumentTypeError: if it is anything other than all the different ways of writing the words true/false.

    Returns:
        transformed_value (bool | None): True, False or None.
    """

    if value is None:
        transformed_value = None
    elif value.lower() == "true":
        transformed_value = True
    elif value.lower() == "false":
        transformed_value = False
    else:
        raise argparse.ArgumentTypeError("Accepted values in ['True', 'true', 'TRue', 'False', 'falSe',...].")

    return transformed_value


def script_arguments(title: str):
    """Function that generates a parser with the parameters taken into account when executing the Python script.

    Args:
        title (str): description of the script.

    Returns:
        argparse.ArgumentParser: parser for this Python script CLI options.
    """

    parser = argparse.ArgumentParser(description=title)

    parser.add_argument("--host-platform",
                        choices = ["linux", "macos", "windows"],
                        type = str,
                        help = "[Mandatory] Specify the host platform",
                        dest = "host_platform")
    parser.add_argument("--linux-host-window-manager",
                        choices = ["x", "wayland"],
                        type = str,
                        help = "[Mandatory for Linux] Specify the host windows manager if the host platform is Linux",
                        dest = "linux_host_window_manager")
    parser.add_argument("--web-browser",
                        choices = ["firefox", "chrome", "edge", "safari", "opera", "brave"],
                        type = str,
                        help = "[Mandatory] Specify the web browser you want to test",
                        dest = "web_browser")
    parser.add_argument("--study",
                        choices = [1, 2, 3],
                        type = int,
                        help = (
                            "[Mandatory] "
                            "1: leaks in popular natively executed web browsers; "
                            "2: leaks in different configurations of a vanilla Firefox; "
                            "3: leaks in different configurations of a compromised Firefox;"
                        ),
                        dest = "study")
    parser.add_argument("--proxy",
                        choices = ["socks", "http-https", "openvpn", "wireguard"],
                        type = str,
                        help = "[Optional] Specify if a proxy is used.",
                        dest = "proxy")
    parser.add_argument("--ip",
                        choices = [4, 6],
                        type = int,
                        help = "[Mandatory if a proxy is set] Specify the IP version used by the proxy tunnel created.",
                        dest = "ip")
    parser.add_argument("--web-browser-containerised",
                        action = "store_true",
                        help = "[Optional] Specify if the leak test is done in a container",
                        dest = "containerised_firefox")
    parser.add_argument("--container-window-manager",
                        choices = ["x", "wayland"],
                        type = str,
                        help = (
                            "[Mandatory if the web browser is containerised] Specify the container windows manager if "
                            "the leak test is done in a container, cannot be wayland if host is macOS"
                        ),
                        dest = "container_window_manager")
    parser.add_argument("--mode",
                        choices = ["default", "forced_mode_2", "forced_mode_3", "forced_mode_4", "compromised"],
                        type = str,
                        help = argparse.SUPPRESS, # [Do not set this argument] Specify the webrtc mode;
                        dest = "mode")
    parser.add_argument("--user-consent",
                        type = user_consent_argument,
                        help = argparse.SUPPRESS, #[Do not set this argument] Specify if there is a user consent or not
                        dest = "user_consent")

    return parser


def validate_arguments(args):
    """Validates the arguments given when the script is run.

    Args:
        args (argparse.Namespace): Arguments given when the script is run.
    """

    parser = argparse.ArgumentParser()

    # Host platform validation
    if args.host_platform is None:
        parser.error("Please specify the host platform.")
    else:
        if args.host_platform == 'linux':
            # Host windows manager validation
            if args.linux_host_window_manager is None:
                parser.error("Please specify the Linux host windows manager.")
            # Container windows manager validation
            elif args.linux_host_window_manager != args.container_window_manager and args.containerised_firefox:
                parser.error("For a Linux host, the window manager must be the same as that of the container.")

        elif args.host_platform in ('macos', 'windows'):
            # Host windows manager validation
            if args.linux_host_window_manager in ('x', 'wayland'):
                parser.error("Do not pass the --linux_host_window_manager option on macOS or Windows.")
            # Container windows manager validation
            if args.containerised_firefox:
                if args.container_window_manager is None:
                    parser.error("Please specify the container windows manager: x for macOS, x or wayland for Windows.")
                elif args.container_window_manager == "wayland" and args.host_platform == "macos":
                    parser.error("macOS does not have a wayland compositor.")

    # Web browser validation
    if args.web_browser is None:
        parser.error("Please specify a web browser.")
    elif args.web_browser != "firefox" and args.containerised_firefox:
        parser.error("The containerised study applies only to Firefox.")

    # Study validation
    if args.study is None:
        parser.error("Please specify a study.")
    else:
        if args.study == 1 and args.containerised_firefox:
            parser.error(
                "The study of a containerised browser cannot be carried out on study 1, which only concerns natively "
                "executed browsers."
            )
        if args.study == 1 and args.proxy is not None:
            parser.error(
                "The study of a containerised browser with a proxy cannot be carried out on study 1, which only "
                "concerns natively executed browsers without proxy."
            )
        if args.study in (2, 3) and args.web_browser != "firefox":
            parser.error("This study applies only to Firefox.")

    # Proxy & IP version validation
    if args.proxy and not args.ip:
        parser.error(
            "A proxy IP network protocol version is required: '4' for IPv4 or '6' for IPv6."
        )
    if args.ip and not args.proxy:
        parser.error(
            "A proxy protocol is required if an IP network protocol version is set."
        )

    # Hidden arguments validation; used when the script is run in a docker container
    if args.mode:
        if args.user_consent is None:
            parser.error("Please set the --user-consent argument: True, False.")
    elif args.mode is None and args.user_consent:
        parser.error(
            "Please specify a mode: ['default', 'forced_mode_2', 'forced_mode_3', 'forced_mode_4', 'compromised')]."
        )


if __name__ == "__main__":

    ARGS = script_arguments("[DEV] WebRTC gather ICE candidates").parse_args()

    print(
        f"Host platform: {ARGS.host_platform}\n"
        f"Linux host window manager: {ARGS.linux_host_window_manager}\n"
        f"Native web browser tested: {ARGS.web_browser}\n"
        f"Wanted proxy's type: {ARGS.proxy}\n"
        f"IP version: {ARGS.ip}\n"
        f"Wanted study: {ARGS.study}\n"
        f"Web browser containerised: {ARGS.containerised_firefox}\n"
        f"Container window manager: {ARGS.container_window_manager}\n"
        f"WebRTC IP handling policy: {ARGS.mode}\n"
        f"getUserMedia() consent: {ARGS.user_consent}"
    )

    validate_arguments(ARGS)

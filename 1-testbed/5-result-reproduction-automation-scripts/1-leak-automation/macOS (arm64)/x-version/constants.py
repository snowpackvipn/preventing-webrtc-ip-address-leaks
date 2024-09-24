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

"""Constants

This module centralises constants containing the paths to the web browsers used, the various WebRTC modes tested and
configurations used in the leak automation script.
"""

__author__ = "Guillaume Nibert"
__credits__ = ["Sébastien Tixeuil", "Baptiste Polvé", "Nana J. Bakalafoua M'boussi", "Xuan Son Nguyen"]
__license__ = "GNU GPLv3"
__maintainer__ = "Guillaume Nibert"
__email__ = "guillaume.nibert@snowpack.eu"

PLATFORMS = {
    "linux-x": "Linux (Ubuntu) - X",
    "linux-wayland": "Linux (Ubuntu) - Wayland",
    "macos": "macOS (arm64)",
    "windows": "Windows"
}

LEAK_STUDIES = {
    1: "1 - Leaks in popular natively executed web browsers",
    2: "2 - Leaks in different configurations of a vanilla Firefox",
    3: "3 - Leaks in different configurations of a compromised Firefox"
}

WEB_BROWSERS = {
    "firefox": "Mozilla Firefox",
    "chrome": "Google Chrome",
    "safari": "Safari",
    "edge": "Microsoft Edge",
    "opera": "Opera",
    "brave": "Brave"
}

OPERA_DRIVER_BIN_PATH = {
    "linux": "utils/operadriver/operadriver_linux64/operadriver",
    "macos": "utils/operadriver/operadriver_mac64/operadriver",
    "windows": "utils/operadriver/operadriver_win64/operadriver.exe",
}

OPERA_BIN_PATH = {
    "linux": "/usr/bin/opera",
    "macos": "/Applications/Opera.app/Contents/MacOS/Opera",
    "windows": "Programs\\Opera\\opera.exe",
}

BRAVE_BIN_PATH = {
    "linux": "/usr/bin/brave-browser",
    "macos": "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
    "windows": "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe",
}

IP_VERSIONS = {4: "IPv4", 6: "IPv6"}

WEBRTC_HANDLING_MODES = {
    1: ["default", "forced_mode_2", "forced_mode_3", "forced_mode_4"],
    2: ["default", "forced_mode_2", "forced_mode_3", "forced_mode_4"],
    3: ["compromised"]
}

USER_CONSENTS = (False, True)

PROXIES = {
    "socks": {
        4: {"address": "198.51.100.1", "port": 1080},
        6: {"address": "2001:db8::2", "port": 1080},
        "name": "SOCKS proxy"
    },
    "http-https": {
        4: {"address": "198.51.100.1", "port": 8081},
        6: {"address": "2001:db8::2", "port": 8081},
        "name": "HTTP-HTTPS proxy"
    },
    "openvpn": {
        4: {"address": "198.51.100.1", "port": 1194},
        6: {"address": "2001:db8::2", "port": 1194},
        "name": "OpenVPN UDP"
    },
    "wireguard": {
        4: {"address": "198.51.100.1", "port": 2050},
        6: {"address": "2001:db8::2", "port": 2050},
        "name": "WireGuard"
    }
}


ICE_CANDIDATES_TXT_DEFAULT_CONF_HEADING = (
    "#########################\n"
    "# Default configuration #\n"
    "#########################"
)
ICE_CANDIDATES_TXT_FORCED_CONF_HEADING = (
    "########################\n"
    "# Forced configuration #\n"
    "########################"
)

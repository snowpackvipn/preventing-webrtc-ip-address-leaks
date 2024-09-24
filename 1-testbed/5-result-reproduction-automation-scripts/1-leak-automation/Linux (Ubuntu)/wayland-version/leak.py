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

"""WebRTC leak automation

This module contains functions that gather automatically all the IP addresses collected by the ICE framework using the
selenium module
"""

__author__ = "Guillaume Nibert"
__credits__ = ["Sébastien Tixeuil", "Baptiste Polvé", "Nana J. Bakalafoua M'boussi", "Xuan Son Nguyen"]
__license__ = "GNU GPLv3"
__maintainer__ = "Guillaume Nibert"
__email__ = "guillaume.nibert@snowpack.eu"


import os
import subprocess
import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from constants import PROXIES, OPERA_DRIVER_BIN_PATH, OPERA_BIN_PATH, BRAVE_BIN_PATH


def webdriver_service(web_browser: str, host_os: str, containerised_firefox: bool):
    """Create the appropriate webdriver service for the chosen web browser.

    Args:
        web_browser (str): accepted values in ["firefox", "chrome", "edge", "safari", "opera", "brave"]
        host_os (str): accepted values in ["linux", "macos", "windows"]
        containerised_firefox (bool): 'True' if Firefox is containerised else 'False'.

    Raises:
        ValueError: At the end of this function run, the webdriver_service variable cannot be None.

    Returns:
        selenium_webdriver_service (selenium.webdriver.service): selenium driver service configured for the chosen web
                                                                 browser.
    """

    if web_browser == "firefox":
        if containerised_firefox and host_os == "macos":
            selenium_webdriver_service = webdriver.FirefoxService("/usr/bin/geckodriver")
        else:
            selenium_webdriver_service = webdriver.FirefoxService()
    elif web_browser in ("chrome", "brave"):
        selenium_webdriver_service = webdriver.ChromeService()
    elif web_browser == "opera":
        selenium_webdriver_service = webdriver.ChromeService(OPERA_DRIVER_BIN_PATH[host_os])
    elif web_browser == "edge":
        selenium_webdriver_service = webdriver.EdgeService()
    elif web_browser == "safari":
        selenium_webdriver_service = webdriver.SafariService()

    if selenium_webdriver_service is None:
        raise ValueError("A selenium webdriver service is required.")

    return selenium_webdriver_service


def web_browser_options(web_browser:str,
                        get_user_media_consent: bool,
                        webrtc_behaviour: str,
                        host_os: str,
                        containerised_firefox: bool,
                        proxy_protocol: str = "",
                        proxy_network_version: int = 0):
    """Configure web browser settings according to the WebRTC handling mode chosen.

    Args:
        web_browser (str): accepted values in ["firefox", "chrome", "edge", "opera", "brave"]
        get_user_media_consent (bool): getUserMedia() consent, 'True' or 'False'.
        webrtc_behaviour (str): ["vanilla", "forced_mode_2", "forced_mode_3", "forced_mode_4" or "compromised"]
        host_os (str): accepted values in ["linux", "macos", "windows"]
        containerised_firefox (bool): 'True' if Firefox is containerised else 'False'.
        proxy_protocol (str, optional): ["socks", "http-https", "openvpn" or "wireguard"]. Defaults to "".
        proxy_network_version (int, optional): accepted values in [4, 6]. Defaults to "".

    Raises:
        ValueError: At the end of this function run, the webrtc_mode_options variable cannot be None.

    Returns:
        webrtc_mode_options (selenium.webdriver.options): web browser settings
    """

    webrtc_mode_options=None

    if web_browser == "firefox":
        webrtc_mode_options = webdriver.FirefoxOptions()

        if containerised_firefox and host_os in ("linux", "windows"):
            webrtc_mode_options.binary_location = "/opt/firefox/firefox"

        webrtc_mode_profile = webdriver.FirefoxProfile()

        # Set up a profile that allows you to authorise or deny access to the camera globally by default, without
        # having to display the prompt to authorise or not, as Selenium does not manage automation on the prompt:
        # https://support.mozilla.org/en-US/kb/how-manage-your-camera-and-microphone-permissions
        if get_user_media_consent:
            webrtc_mode_profile.set_preference("permissions.default.microphone", 1)  # 1: allow
            webrtc_mode_profile.set_preference("permissions.default.camera", 1)
        else:
            webrtc_mode_profile.set_preference("permissions.default.microphone", 2)  # 2: deny
            webrtc_mode_profile.set_preference("permissions.default.camera", 2)

        # Mozilla Firefox WebRTC IP handling policy: https://wiki.mozilla.org/Media/WebRTC/Privacy
        if webrtc_behaviour == "forced_mode_2":
            webrtc_mode_profile.set_preference("media.peerconnection.ice.default_address_only", True)
        elif webrtc_behaviour == "forced_mode_3":
            webrtc_mode_profile.set_preference("media.peerconnection.ice.default_address_only", True)
            webrtc_mode_profile.set_preference("media.peerconnection.ice.no_host", True)
        elif webrtc_behaviour == "forced_mode_4":
            webrtc_mode_profile.set_preference("media.peerconnection.ice.proxy_only", True)
        elif webrtc_behaviour == "compromised":
            webrtc_mode_profile.set_preference("media.peerconnection.ice.obfuscate_host_addresses", False)
            webrtc_mode_profile.set_preference("media.peerconnection.ice.proxy_only", False)
            webrtc_mode_profile.set_preference("media.peerconnection.ice.link_local", True)
            webrtc_mode_profile.set_preference("media.peerconnection.ice.loopback", True)
            webrtc_mode_profile.set_preference("media.peerconnection.ice.proxy_only_if_behind_proxy", False)
            webrtc_mode_profile.set_preference("media.peerconnection.ice.relay_only", False)
            webrtc_mode_profile.set_preference("media.peerconnection.ice.force_interface", "")
            webrtc_mode_profile.set_preference("media.peerconnection.ice.relay_only", False)
            webrtc_mode_profile.set_preference("media.peerconnection.use_document_iceservers", True)
            webrtc_mode_profile.set_preference("media.peerconnection.ice.default_address_only", False)
            webrtc_mode_profile.set_preference("media.peerconnection.ice.no_host", False)
            webrtc_mode_profile.set_preference("media.peerconnection.enabled", True)
            webrtc_mode_profile.set_preference("media.peerconnection.ice.tcp", True)
            webrtc_mode_profile.set_preference("media.peerconnection.identity.enabled", True)
            webrtc_mode_profile.set_preference("media.peerconnection.turn.disable", False)
            webrtc_mode_profile.set_preference("media.peerconnection.allow_old_setParameters", True)

        # Set up the integrated SOCKS or HTTP-HTTPS proxy client:
        if proxy_protocol in ("http-https", "socks") and proxy_network_version:

            # Manual proxy configuration: # https://kb.mozillazine.org/Network.proxy.type
            webrtc_mode_profile.set_preference("network.proxy.type", 1)

            if proxy_protocol == "http-https":
                webrtc_mode_profile.set_preference(
                    "network.proxy.http", PROXIES[proxy_protocol][proxy_network_version]["address"]
                )
                webrtc_mode_profile.set_preference(
                    "network.proxy.http_port", PROXIES[proxy_protocol][proxy_network_version]["port"]
                )
                webrtc_mode_profile.set_preference(
                    "network.proxy.ssl", PROXIES[proxy_protocol][proxy_network_version]["address"]
                )
                webrtc_mode_profile.set_preference(
                    "network.proxy.ssl_port", PROXIES[proxy_protocol][proxy_network_version]["port"]
                )
                # The MITM Proxy provide a certificate authority to trust
                webrtc_mode_options.add_argument('--ignore-certificate-errors')

            elif proxy_protocol == "socks":
                webrtc_mode_profile.set_preference("network.proxy.socks_version", 5)
                webrtc_mode_profile.set_preference(
                    "network.proxy.socks", PROXIES[proxy_protocol][proxy_network_version]["address"]
                )
                webrtc_mode_profile.set_preference(
                    "network.proxy.socks_port", PROXIES[proxy_protocol][proxy_network_version]["port"]
                )
                webrtc_mode_profile.set_preference("network.proxy.socks_remote_dns", True)  # Proxy DNS through SOCKSv5

        webrtc_mode_options.profile = webrtc_mode_profile

    # Chromium-based browsers
    elif web_browser in ("chrome", "edge", "brave", "opera"):

        if web_browser == "edge":
            webrtc_mode_options = webdriver.EdgeOptions()
        else:
            webrtc_mode_options = webdriver.ChromeOptions()
            if web_browser == "opera":
                if host_os == "windows":
                    appdata_local_dir = os.getenv("LOCALAPPDATA")
                    webrtc_mode_options.binary_location = f"{appdata_local_dir}\\{OPERA_BIN_PATH[host_os]}"
                else:
                    web_browser_options.binary_location = OPERA_BIN_PATH[host_os]
                webrtc_mode_options.add_experimental_option('w3c', True)
            elif web_browser == "brave":
                webrtc_mode_options.binary_location = BRAVE_BIN_PATH[host_os]

        preferences = {}

        # Set up a profile that allows you to authorise or deny access to the camera globally by default, without
        # having to display the prompt to authorise or not, as Selenium does not manage automation on the prompt:
        # https://support.google.com/chrome/answer/2693767?hl=en-gb
        if get_user_media_consent:
            preferences = {
                "profile.default_content_setting_values.media_stream_mic": 1,  # 1: allow
                "profile.default_content_setting_values.media_stream_camera": 1
            }
        else:
            preferences = {
                "profile.default_content_setting_values.media_stream_mic": 2,  # 2: deny
                "profile.default_content_setting_values.media_stream_camera": 2
            }

        # Chromium-based browser WebRTC IP handling policy:
        # https://developer.chrome.com/docs/extensions/mv2/reference/privacy#type-IPHandlingPolicy
        if webrtc_behaviour == "forced_mode_2":
            preferences["webrtc.ip_handling_policy"] = "default_public_and_private_interfaces"
        elif webrtc_behaviour == "forced_mode_3":
            preferences["webrtc.ip_handling_policy"] = "default_public_interface_only"
        elif webrtc_behaviour == "forced_mode_4":
            preferences["webrtc.ip_handling_policy"] = "disable_non_proxied_udp"

        webrtc_mode_options.add_experimental_option("prefs", preferences)

    if webrtc_mode_options is None:
        raise ValueError("The webrtc_mode_options cannot be None.")

    return webrtc_mode_options


def selenium_webdriver(web_browser:str, webdriver_options, selenium_webdriver_service):
    """Create the appropriate webdriver for the browser and loads the parameters defined in the webdriver options.

    Args:
        web_browser (str): accepted values in ["firefox", "chrome", "edge", "safari", "opera", "brave"]
        webrtc_mode_options (selenium.webdriver.options): web browser settings

    Raises:
        ValueError: At the end of this function run, the driver variable cannot be None.

    Returns:
        driver (selenium.webdriver): selenium driver configured for the chosen web browser with the chosen parameters.
    """

    driver = None

    if web_browser == "firefox":
        driver = webdriver.Firefox(options=webdriver_options, service=selenium_webdriver_service)
    elif web_browser in ("chrome", "brave", "opera"):
        driver = webdriver.Chrome(options=webdriver_options, service=selenium_webdriver_service)
    elif web_browser == "edge":
        driver = webdriver.Edge(options=webdriver_options, service=selenium_webdriver_service)
    elif web_browser == "safari":
        driver = webdriver.Safari(options=webdriver_options, service=selenium_webdriver_service)

    if driver is None:
        raise ValueError("A selenium driver is required.")

    return driver


def run_leak(web_browser:str,
             selenium_webdriver_service,
             get_user_media_consent: bool,
             webrtc_behaviour: str,
             host_os,
             containerised_firefox,
             proxy_protocol: str = "",
             proxy_network_version: int = 0) -> list:
    """Retrieves ICE candidates by executing the functions in the gather_ice_candidates.js script

    Args:
        web_browser (str): accepted values in ["firefox", "chrome", "edge", "safari", "opera", "brave"]
        selenium_webdriver_service (selenium.webdriver.service): selenium driver service configured for the web browser.
        get_user_media_consent (bool): getUserMedia() consent, 'True' or 'False'.
        webrtc_behaviour (str): ["vanilla", "forced_mode_2", "forced_mode_3", "forced_mode_4" or "compromised"]
        host_os (str): accepted values in ["linux", "macos", "windows"]
        containerised_firefox (bool): 'True' if Firefox is containerised else 'False'.
        proxy_protocol (str, optional): ["socks", "http-https", "openvpn" or "wireguard"]. Defaults to "".
        proxy_network_version (str, optional): accepted values in [4, 6]. Defaults to "".

    Returns:
        result_list (list): list of ICE candidate addresses.
    """

    result_list = []

    if host_os == "macos" and web_browser == "safari":
        safari_command = ["/Applications/Safari.app/Contents/MacOS/Safari"]

        with subprocess.Popen(safari_command) as safari_process:

            time.sleep(5)

            print(
                "\n\nSafari automation is semi-automated, please authorise all automation-related requests "
                "(camera/microphone, automation...) within 10 seconds. If this duration is exceeded, please restart the "
                "script.\n\n"
            )

            safari_open_gather_ice_candidate_page_command = [
                'osascript',
                '-e', 'tell application "Safari" to activate',
                '-e', f'tell application "Safari" to tell window 1 to tell current tab to set URL '
                f'to "file://{os.getcwd()}/gather_ice_candidates/'
                f'index_safari_user_consent_{get_user_media_consent}.html"',
                '-e', 'delay 10',
                '-e', 'tell application "System Events" to key code 48',
                '-e', 'delay 1',
                '-e', 'tell application "System Events" to keystroke "a" using {command down}',
                '-e', 'delay 1',
                '-e', 'tell application "System Events" to keystroke "c" using {command down}',
                '-e', 'delay 1',
                '-e', 'tell application "Safari" to quit'
            ]

            with subprocess.Popen(
                safari_open_gather_ice_candidate_page_command
            ) as safari_open_gather_ice_candidate_page_command:
                safari_open_gather_ice_candidate_page_command.wait()

            safari_process.wait()

        result_list = subprocess.check_output('pbpaste').decode('utf-8').split(",")[:-1]
        print(f"Safari result list: {result_list}")

    else:
        webdriver_options = web_browser_options(
            web_browser,
            get_user_media_consent,
            webrtc_behaviour,
            host_os,
            containerised_firefox,
            proxy_protocol,
            proxy_network_version)

        driver = selenium_webdriver(web_browser, webdriver_options, selenium_webdriver_service)

        driver.get(f"file:///{os.getcwd()}/gather_ice_candidates/index.html")

        if get_user_media_consent:
            results = driver.execute_script('stun_with_getusermedia(); turn_with_getusermedia()')
        else:
            results = driver.execute_script('stun_without_getusermedia(); turn_without_getusermedia()')

        try:
            WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.ID, "ice_candidates"))
            )
            time.sleep(5)
            results = driver.find_element(By.ID, "ice_candidates").get_attribute('innerHTML')
            result_list = results.split(",")[:-1]
        except TimeoutException as selenium_timeout_exception:
            print(f"Error in finding ICE candidates: {selenium_timeout_exception}")
            result_list = []

        if web_browser == "brave":
            driver.close()

        driver.quit()

        if not result_list:
            result_list = ["No ICE candidate found."]

    return result_list


if __name__ == "__main__":

    WEB_BROWSER = "firefox"
    HOST_OS = "linux"
    CONTAINERISED_FIREFOX = False
    WEBRTC_BEHAVIOUR = "forced_mode_2"
    GET_USER_MEDIA_CONSENT = True
    PROXY_PROTOCOL = "http-https"
    PROXY_NETWORK_VERSION = 4

    WEBDRIVER_SERVICE = webdriver_service(WEB_BROWSER, HOST_OS, CONTAINERISED_FIREFOX)

    RESULTS = run_leak(WEB_BROWSER,
                       WEBDRIVER_SERVICE,
                       GET_USER_MEDIA_CONSENT,
                       WEBRTC_BEHAVIOUR,
                       HOST_OS,
                       CONTAINERISED_FIREFOX,
                       PROXY_PROTOCOL,
                       PROXY_NETWORK_VERSION)

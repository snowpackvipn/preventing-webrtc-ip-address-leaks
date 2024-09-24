#!/usr/bin/python3
# coding: utf-8
#
# Benchmarks
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

"""Run the performance benchmarks several times.

This module contains scripts that allow the JetStream 2.2, MotionMark 1.3 and Speedometer 3.0 benchmarks to be run 
several times automatically.

The run_BENCHMARKNAME_benchmark procedures are adapted from those provided by phoronix-test-suite under licence GPL-3.0:
http://phoronix-test-suite.com/benchmark-files/selenium-scripts-10.zip
Phoronix Test Suite:
    URLs: http://www.phoronix.com, http://www.phoronix-test-suite.com/
    Copyright 2008 - 2024 by Phoronix Media.
    Lead Architects:
        - Michael Larabel <michael@phoronix.com>
        - Matthew Tippett <matthew@phoronix.com>
    There's also other individuals and organizations who have contributed patches, ideas, and made other contributions
    to the Phoronix Test Suite.
"""

__author__ = "Guillaume Nibert"
__credits__ = ["Sébastien Tixeuil", "Baptiste Polvé", "Nana J. Bakalafoua M'boussi", "Xuan Son Nguyen"]
__license__ = "GNU GPLv3"
__maintainer__ = "Guillaume Nibert"
__email__ = "guillaume.nibert@snowpack.eu"

import os
import argparse
import time
import datetime
import json

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

DEBUG = False


def firefox_vanilla_profile(download_dir: str):
    """Create a vanilla Firefox profile with a specific download directory to save the benchmark results

    Returns:
        vanilla_options (selenium.webdriver.firefox.options): Vanilla Firefox profile
    """
    vanilla_options=Options()
    vanilla_profile = FirefoxProfile()
    vanilla_profile.set_preference("browser.download.folderList", 2)
    vanilla_profile.set_preference("browser.download.manager.showWhenStarting", False)
    vanilla_profile.set_preference("browser.download.dir", download_dir)
    vanilla_profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")
    vanilla_options.profile = vanilla_profile

    return vanilla_options

def firefox_compromised_profile(download_dir: str):
    """Create a compromised Firefox profile with a specific download directory to save the benchmark results

    Returns:
        compromised_options: (selenium.webdriver.firefox.options): Compromised Firefox profile
    """

    compromised_options=Options()
    compromised_profile = FirefoxProfile()
    compromised_profile.set_preference("browser.download.folderList", 2)
    compromised_profile.set_preference("browser.download.manager.showWhenStarting", False)
    compromised_profile.set_preference("browser.download.dir", download_dir)
    compromised_profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")

    compromised_profile.set_preference("media.peerconnection.ice.obfuscate_host_addresses", False)
    compromised_profile.set_preference("media.peerconnection.ice.proxy_only", False)
    compromised_profile.set_preference("media.peerconnection.ice.link_local", True)
    compromised_profile.set_preference("media.peerconnection.ice.loopback", True)
    compromised_profile.set_preference("media.peerconnection.ice.proxy_only_if_behind_proxy", False)
    compromised_profile.set_preference("media.peerconnection.ice.relay_only", False)
    compromised_profile.set_preference("media.peerconnection.ice.force_interface", "")
    compromised_profile.set_preference("media.peerconnection.ice.relay_only", False)
    compromised_profile.set_preference("media.peerconnection.use_document_iceservers", True)
    compromised_profile.set_preference("media.peerconnection.ice.default_address_only", False)
    compromised_profile.set_preference("media.peerconnection.ice.no_host", False)
    compromised_profile.set_preference("media.peerconnection.enabled", True)
    compromised_profile.set_preference("media.peerconnection.ice.tcp", True)
    compromised_profile.set_preference("media.peerconnection.identity.enabled", True)
    compromised_profile.set_preference("media.peerconnection.turn.disable", False)
    compromised_profile.set_preference("media.peerconnection.allow_old_setParameters", True)

    compromised_options.profile = compromised_profile

    return compromised_options


def run_jetstream_benchmark(options_profile, selenium_service) -> str:
    """Run the JetStream 2.2 benchmark once.

    Args:
        options_profile (selenium.webdriver.firefox.options): Selenium Firefox profile and binary
        selenium_service (selenium.webdriver.firefox.options): Selenium Firefox service (geckodriver)

    Returns:
        str: results (in JSON format)
    """
    driver = webdriver.Firefox(options=options_profile, service=selenium_service)
    driver.maximize_window()
    driver.get("https://browserbench.org/JetStream2.2/")

    WebDriverWait(driver, 1200).until(
            EC.visibility_of_element_located((By.XPATH, "//*[text()='Start Test']"))
        )

    driver.find_element(By.XPATH, "//*[text()='Start Test']").click()
    WebDriverWait(driver, 1200).until(
            EC.visibility_of_element_located((By.ID, "result-summary"))
        )

    results = driver.execute_script("return JetStream.resultsJSON()")

    print("JSON JetStream 2.2", results)

    driver.quit()

    return results


def run_motionmark_benchmark(options_profile, selenium_service) -> dict:
    """Run the MotionMark 1.3 benchmark once.

    Args:
        options_profile (selenium.webdriver.firefox.options): Selenium Firefox profile and binary
        selenium_service (selenium.webdriver.firefox.options): Selenium Firefox service (geckodriver)

    Returns:
        dict: results
    """

    driver = webdriver.Firefox(options=options_profile, service=selenium_service)
    driver.maximize_window()
    driver.fullscreen_window()

    driver.get("https://browserbench.org/MotionMark1.3/developer.html")

    WebDriverWait(driver, 1200).until(
            EC.visibility_of_element_located((By.ID, "suite-0"))
        )
    checkbox = driver.find_element(By.ID, "suite-0")

    ActionChains(driver).move_to_element(checkbox).click(checkbox).perform()
    time.sleep(1)

    driver.execute_script("return benchmarkController.startBenchmark();")
    WebDriverWait(driver, 1200).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "score"))
            )
    score_fps = driver.find_element(By.CLASS_NAME, "score").text.split(" @ ")
    score = float(score_fps[0])
    fps = float(score_fps[1][:-3])

    confidence_interval = driver.find_element(By.CLASS_NAME, "confidence").text.split(" / ")
    confidence_interval_lower_bound = float(confidence_interval[0][1:-1])
    confidence_interval_upper_bound = float(confidence_interval[1][1:-1])

    print(f"MotionMark Score: {score}")
    print(f"MotionMark 80% Confidence Interval: {confidence_interval}")

    header_table = driver.find_element(By.ID, "results-header")
    score_table = driver.find_element(By.ID, "results-score")
    other_data_table = driver.find_element(By.ID, "results-data")

    # Extract data
    score_data = []
    other_data = []

    for score_row in score_table.find_elements(By.TAG_NAME, "tr")[2:]:
        score = float(score_row.find_element(By.TAG_NAME, "td").text)

        score_data.append(score)

    # Extract data table rows
    for i, other_data_row in enumerate(other_data_table.find_elements(By.TAG_NAME, "tr")[2:]): # remove up to suites-separator

        other_data_row_line = other_data_row.find_elements(By.TAG_NAME, "td")

        other_data_row_line_list = []

        for j, cell in enumerate(other_data_row_line):

        # Skip separator rows
            if cell.get_attribute("class") != "suites-separator":
                if j in (1, 5, 7):
                    other_data_row_line_list.append(float(cell.text))
                elif j == 2:
                    other_data_row_line_list.append(float(cell.text[2:]))
                elif j in (3, 4):
                    other_data_row_line_list.append(float(cell.text[1:-1]))
                elif j == 6:
                    other_data_row_line_list.append(float(cell.text[2:-1]))
                elif j == 8:
                    other_data_row_line_list.append(float(cell.text[2:-2]))

        other_data.append(other_data_row_line_list)

    motionmark_data = {}
    for i, header_row in enumerate(header_table.find_elements(By.TAG_NAME, "tr")[2:]):  # remove up to suites-separator
        # Check if it's a data row (not a separator)
        header = header_row.find_element(By.TAG_NAME, "td").text

        motionmark_data[header] = {}

        motionmark_data[header]['Score'] = score_data[i]
        motionmark_data[header]['80 percent CI'] = {
            'min': other_data[i][0],
            'max': other_data[i][1],
            'percentMin': other_data[i][2],
            'percentMax': other_data[i][3]
        }
        motionmark_data[header]['Time Complexity'] = {
            'average': other_data[i][4],
            'percent': other_data[i][5]
        }
        motionmark_data[header]['Raw Complexity'] = {
            'average': other_data[i][6],
            'stdev': other_data[i][7]
        }

    motionmark_data['Global Score'] = {
        'Geomean': score,
        'fps': fps,
        '80 CI lower percentage': confidence_interval_lower_bound,
        '80 CI upper percentage': confidence_interval_upper_bound
    }

    driver.quit()

    return motionmark_data


def run_speedometer_benchmark(options_profile, selenium_service):
    """Run the Speedometer 3.0 benchmark once.

    Args:
        options_profile (selenium.webdriver.firefox.options): Selenium Firefox profile and binary
        selenium_service (selenium.webdriver.firefox.options): Selenium Firefox service (geckodriver)

    """
    driver = webdriver.Firefox(options=options_profile, service=selenium_service)
    driver.maximize_window()
    driver.get("https://browserbench.org/Speedometer3.0/")

    WebDriverWait(driver, 1200).until(
            EC.visibility_of_element_located((By.XPATH, "//*[text()='Start Test']"))
        )

    driver.find_element(By.XPATH, "//*[text()='Start Test']").click()
    WebDriverWait(driver, 1200).until(
            EC.visibility_of_element_located((By.XPATH, "//*[text()='Details']"))
            )

    driver.find_element(By.XPATH, "//*[text()='Details']").click()

    driver.find_element(By.XPATH, "//*[text()='Download JSON']").click()

    driver.find_element(By.XPATH, "//*[text()='Summary']").click()

    results = driver.find_element(By.ID, "result-number")
    print(f"Speedometer 3.0 result: {results.text}")

    driver.quit()


def run_multiple_benchmarks(benchmark_name: str,
                            options_profile,
                            selenium_service,
                            benchmark_data_dir: str,
                            nb_of_benchmarks: int=20):
    """Run the selected benchmark several times.

    Args:
        benchmark_name (str): name of the benchmark; 'jetstream2', 'motionmark' or 'speedometer3'
        options_profile (selenium.webdriver.firefox.options): selenium Firefox profile and binary
        selenium_service (selenium.webdriver.firefox.options): selenium Firefox service (geckodriver)
        benchmark_data_dir (str): benchmark data json file folder
        nb_of_benchmarks (int, optional): number of benchmarks to be performed. Defaults to 20.
    """

    if benchmark_name == "jetstream2":
        for _ in range(nb_of_benchmarks):
            jetstream_date_string = datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
            jetstream_data_to_be_written = run_jetstream_benchmark(options_profile, selenium_service)
            with open(f"{benchmark_data_dir}/jetstream-{jetstream_date_string}.json", "w", encoding="utf8") as outfile:
                outfile.write(jetstream_data_to_be_written)
    elif benchmark_name == "motionmark":
        for _ in range(nb_of_benchmarks):
            motionmark_date_string = datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
            motionmark_data_to_be_written = run_motionmark_benchmark(options_profile, selenium_service)
            with open(f"{benchmark_data_dir}/motionmark-{motionmark_date_string}.json", "w", encoding="utf8") as outfile:
                json.dump(motionmark_data_to_be_written, outfile)
    elif benchmark_name == "speedometer3":
        for _ in range(nb_of_benchmarks):
            run_speedometer_benchmark(options_profile, selenium_service)


def validate_arguments(args):
    """Validates the arguments given when the script is run. If the script is run in the contianer

    Args:
        args (argparse.Namespace): Arguments given when the script is run.
    """

    parser = argparse.ArgumentParser()

    if args.host_platform is None:
        parser.error("Please specify the host platform.")
    if args.host_platform == 'linux' and args.linux_host_window_manager is None:
        parser.error("Please specify the Linux host windows manager.")
    if args.host_platform in ('x', 'wayland') and args.host_platform in ('macos', 'windows'):
        parser.error("Do not pass the --linux_host_window_manager option on macOS or Windows.")
    if (args.container_window_manager is None
            and args.web_browser_containerised
            and args.host_platform in ("macos", "windows")):
        parser.error("Please specify the Linux container windows manager.")
    if args.host_platform == 'linux' and args.web_browser_containerised:
        args.container_window_manager = args.linux_host_window_manager
    if (args.host_platform == 'linux'
            and args.web_browser_containerised
            and args.container_window_manager != args.linux_host_window_manager):
        parser.error("For a Linux host, the window manager must be the same as that of the container.")
    if args.container_window_manager == "wayland" and args.host_platform == "macos":
        parser.error("macOS does not have a wayland compositor.")

if __name__ == "__main__":

    PARSER = argparse.ArgumentParser(description="Benchmarks automation")
    PARSER.add_argument("--host-platform",
                        choices = ["linux", "macos", "windows"],
                        type = str,
                        help = "Specify the host platform",
                        dest = "host_platform")
    PARSER.add_argument("--linux-host-window-manager",
                        choices = ["x", "wayland"],
                        type = str,
                        help = "Specify the host windows manager if the host platform is Linux",
                        dest = "linux_host_window_manager")
    PARSER.add_argument("--benchmark",
                        choices = ["jetstream2", "motionmark", "speedometer3"],
                        type = str,
                        help= "Select the desired benchmark")
    PARSER.add_argument("--web-browser-containerised",
                        action = "store_true",
                        help = "Specify if the benchmark is done in a container",
                        dest = "web_browser_containerised")
    PARSER.add_argument("--container-window-manager",
                        choices = ["x", "wayland"],
                        type = str,
                        help = "Specify the container windows manager if the benchmark is done in a container on macOS"
                            " and Windows, cannot be wayland if host is macOS",
                        dest = "container_window_manager")

    ARGS = PARSER.parse_args()

    validate_arguments(ARGS)

    if DEBUG:
        print(f"Host platform: {ARGS.host_platform}")
        print(f"Linux host window manager: {ARGS.linux_host_window_manager}")
        print(f"Benchmark name: {ARGS.benchmark}")
        print(f"Web browser containerised: {ARGS.web_browser_containerised}")
        print(f"Container window manager: {ARGS.container_window_manager}")

    PLATFORMS = {
        'linux': 'Linux (Ubuntu)',
        'macos': 'macOS (arm64)',
        'windows': 'Windows'
    }

    PLATFORM = PLATFORMS[ARGS.host_platform]

    ENVIRONMENT = ""

    if ARGS.web_browser_containerised:
        ENVIRONMENT = f"docker-{ARGS.container_window_manager}"
    elif not ARGS.web_browser_containerised and ARGS.host_platform == "linux":
        ENVIRONMENT = f"host-{ARGS.linux_host_window_manager}"
    elif not ARGS.web_browser_containerised and ARGS.host_platform in ("macos", "windows"):
        ENVIRONMENT = "host"


    ################
    # DOWNLOAD DIR #
    ################

    # The only folder shared with the host is the Download folder, so the results are saved in this folder.
    HOME = os.path.expanduser("~")

    DOWNLOAD_VANILLA_DIR = f"{HOME}/Downloads/2-performance-data/{PLATFORM}/{ENVIRONMENT}/vanilla/{ARGS.benchmark}"
    DOWNLOAD_COMPROMISED_DIR = (
        f"{HOME}/Downloads/2-performance-data/{PLATFORM}/{ENVIRONMENT}/compromised/{ARGS.benchmark}"
    )

    if not ARGS.web_browser_containerised and ARGS.host_platform == "windows" and ARGS.benchmark == "speedometer3":
        DOWNLOAD_VANILLA_DIR = (
            f"{HOME}\\Downloads\\2-performance-data\\{PLATFORM}\\{ENVIRONMENT}\\vanilla\\{ARGS.benchmark}"
        )
        DOWNLOAD_COMPROMISED_DIR = (
            f"{HOME}\\Downloads\\2-performance-data\\{PLATFORM}\\{ENVIRONMENT}\\compromised\\{ARGS.benchmark}"
        )

    if not os.path.exists(DOWNLOAD_VANILLA_DIR):
        os.makedirs(DOWNLOAD_VANILLA_DIR, exist_ok=True)  # Create directories recursively

    if not os.path.exists(DOWNLOAD_COMPROMISED_DIR):
        os.makedirs(DOWNLOAD_COMPROMISED_DIR, exist_ok=True)  # Create directories recursively

    print(f"DOWNLOAD_VANILLA_DIR: {DOWNLOAD_VANILLA_DIR}")
    print(f"DOWNLOAD_COMPROMISED_DIR: {DOWNLOAD_COMPROMISED_DIR}")

    selenium_vanilla_firefox_options = firefox_vanilla_profile(DOWNLOAD_VANILLA_DIR)
    selenium_compromised_firefox_options = firefox_compromised_profile(DOWNLOAD_COMPROMISED_DIR)

    selenium_firefox_service = Service()

    if ARGS.web_browser_containerised and ARGS.host_platform in ("linux", "windows"):
        selenium_vanilla_firefox_options.binary_location = "/opt/firefox/firefox"
        selenium_compromised_firefox_options.binary_location = "/opt/firefox/firefox"
    elif ARGS.web_browser_containerised and ARGS.host_platform == "macos":
        selenium_vanilla_firefox_options.binary_location = "/usr/bin/firefox"
        selenium_compromised_firefox_options.binary_location = "/usr/bin/firefox"
        selenium_firefox_service = Service("/usr/bin/geckodriver")

    ##############################################################
    # Run the selected benchmark with a vanilla Firefox 20 times #
    ##############################################################
    print("Vanilla Firefox benchmark")
    run_multiple_benchmarks(ARGS.benchmark,
                            selenium_vanilla_firefox_options,
                            selenium_firefox_service,
                            DOWNLOAD_VANILLA_DIR,
                            20)

    ##################################################################
    # Run the selected benchmark with a compromised Firefox 20 times #
    ##################################################################
    print("Compromised Firefox benchmark")
    run_multiple_benchmarks(ARGS.benchmark,
                            selenium_compromised_firefox_options,
                            selenium_firefox_service,
                            DOWNLOAD_COMPROMISED_DIR,
                            20)

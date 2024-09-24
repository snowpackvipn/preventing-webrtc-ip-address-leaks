#!/usr/bin/python3
# coding: utf-8
#
# Copyright (C) 2024 Guillaume Nibert <guillaume.nibert@snowpack.eu>,
#                    Sébastien Tixeuil <sebastien.tixeuil@lip6.fr>,
#                    Baptiste Polvé <baptiste.polve@snowpack.eu>,
#                    Nana J. Bakalafoua M'boussi <nana.bakalafoua@snowpack.eu>,
#                    Xuan Son Nguyen <xuanson.nguyen@snowpack.eu>
#
# This file is part of Benchmark graphs.
#
# Benchmark graphs is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# Benchmark graphs is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Benchmark graphs. If not, see <https://www.gnu.org/licenses/>.

"""Benchmark data

This module contains the raw data, averages, confidence intervals and ratios associated with the JetStream2.3,
MotionMark1.3 and Speedometer3 benchmarks.
"""

__author__ = "Guillaume Nibert"
__credits__ = ["Sébastien Tixeuil", "Baptiste Polvé", "Nana J. Bakalafoua M'boussi", "Xuan Son Nguyen"]
__license__ = "GNU GPLv3"
__maintainer__ = "Guillaume Nibert"
__email__ = "guillaume.nibert@snowpack.eu"

import os
import json
from pathlib import Path

import numpy as np

from scipy.special import stdtrit

DEBUG = False
DATA_BASE_DIR = f"{Path(__file__).parents[2]}/3-raw-data/2-performance-data"


def confidence_interval_sample(values: list, arithmetic_mean: float, confidence_level: float=0.95) -> list:
    """Calculation of the confidence interval for a sample.

    Args:
        values (list): score list.
        arithmetic_mean (float): arithmetic mean of the scores in the list.
        conf (float, optional): desired confidence. Defaults to 0.95 (for a 95% confidence interval).
    """

    # http://www.stat.yale.edu/Courses/1997-98/101/confint.htm
    # /2 because its a two-tailed CI # https://www.scribbr.com/statistics/confidence-interval/
    alpha = (1 - confidence_level) / 2
    # Probability associated with the two-tailed Student's t-distribution.
    probability = 1 - alpha
    number_of_experiments = len(values)

    # For a sample: (number_of_experiments - 1); For a population: (number_of_experiments)
    corrected_sample_variance = sum([(value - arithmetic_mean)**2 for value in values]) / (number_of_experiments - 1)
    standard_deviation = np.sqrt(corrected_sample_variance)

    degrees_of_freedom = number_of_experiments - 1

    # scipy.special.stdtrit: inverse cumulative distribution function (CDF) for the Student's T-Distribution table
    quantile = stdtrit(degrees_of_freedom, probability)
    confidence_interval_delta = quantile*(standard_deviation/np.sqrt(number_of_experiments))
    confidence_interval = [arithmetic_mean - confidence_interval_delta, arithmetic_mean + confidence_interval_delta]

    return confidence_interval


def calculate_arithmetic_mean(values: list) -> float:
    """Calculation of the arithmetic mean of a list of values.

    Args:
        values (list): list of values.

    Returns:
        float: arithmetic mean of a list of values.
    """
    return sum(values)/len(values)


def performance_ratio(host_mean: float, docker_mean: float) -> float:
    """Calculation of the performance ratio of a native mean score to the associated docker mean score.

    Args:
        host_mean (float): native mean score.
        docker_mean (float): docker mean score.

    Returns:
        float: performance ratio of a native mean score to the associated docker mean score.
    """

    return host_mean/docker_mean


def get_benchmark_score(benchmark: str, path: str) -> float:
    """Retrieve the score for one of the three benchmarks from the JSON associated with the benchmark.

    Args:
        benchmark (str): benchmark name; allowed values: 'jetstream2', 'motionmark' or 'speedometer3'.
        path (str): path to the JSON file containing the raw data results of the benchmark.

    Returns:
        float: benchmark score.
    """

    score = 0.0

    with open(path, "r", encoding="utf8") as file:
        benchmark_data = json.load(file)

    if benchmark == "jetstream2":
        product_of_results = 1.0
        nb_of_tests = len(benchmark_data["JetStream2.0"]["tests"])

        for test in benchmark_data["JetStream2.0"]["tests"]:
            product_of_results *= benchmark_data["JetStream2.0"]["tests"][test]["metrics"]["Score"]["current"][0]

        score = product_of_results**(1/nb_of_tests)
    elif benchmark == 'motionmark':
        score = benchmark_data["Global Score"]["Geomean"]
    elif benchmark == 'speedometer3':
        score = benchmark_data["Score"]["mean"]
    else:
        raise ValueError("Benchmark parameter authorised values are: 'jetstream2', 'motionmark' or 'speedometer3'")

    return score


##########################
# General data structure #
##########################

# benchmark_name_data = {
#     'raw_data': {},
#     'means': {},
#     'confidence_intervals' : {},
#     'means_in_confidence_intervals': {},
#     'performance_ratios': {}
# }


#############################
# JetStream2 data structure #
#############################

# jetstream2_data = {
#     'raw_data': {  # scores of 20 benchmark executions
#         'linux_host_firefox_wayland_jetstream2': [
#             113.778, 119.012, 119.389, 114.611, 115.823,
#             112.431, 113.314, 118.417, 113.374, 113.765,
#             115.504, 114.992, 116.728, 109.464, 112.245
#         ],
#         'linux_docker_firefox_wayland_jetstream2': [
#             120.250, 118.864, 120.910, 119.235, 116.838,
#             115.046, 119.439, 119.054, 120.866, 117.485,
#             117.937, 118.553, 115.491, 115.117, 114.045
#         ],
#         'linux_host_compromised_firefox_wayland_jetstream2': list(float),
#         'linux_docker_compromised_firefox_wayland_jetstream2': list(float),
#         'linux_host_firefox_x_jetstream2': list(float),
#         'linux_docker_firefox_x_jetstream2': list(float),
#         'linux_host_compromised_firefox_x_jetstream2': list(float),
#         'linux_docker_compromised_firefox_x_jetstream2': list(float),
#         'macos_host_firefox_jetstream2': list(float),
#         'macos_docker_firefox_x_jetstream2': list(float),
#         'macos_host_compromised_firefox_jetstream2': list(float),
#         'macos_docker_compromised_firefox_x_jetstream2': list(float),
#         'windows_host_firefox_jetstream2': list(float),
#         'windows_docker_firefox_wayland_jetstream2': list(float),
#         'windows_docker_firefox_x_jetstream2': list(float),
#         'windows_host_compromised_firefox_jetstream2': list(float),
#         'windows_docker_compromised_firefox_wayland_jetstream2': list(float),
#         'windows_docker_compromised_firefox_x_jetstream2': list(float),
#     },
#     'means': {  # Arithmetric mean of 20 benchmark execution
#         'linux_host_firefox_wayland_jetstream2': 114.856,
#         'linux_docker_firefox_wayland_jetstream2': 117.942,
#         'linux_host_compromised_firefox_wayland_jetstream2': float,
#         'linux_docker_compromised_firefox_wayland_jetstream2': float,
#         'linux_host_firefox_x_jetstream2': float,
#         'linux_docker_firefox_x_jetstream2': float,
#         'linux_host_compromised_firefox_x_jetstream2': float,
#         'linux_docker_compromised_firefox_x_jetstream2': float,
#         'macos_host_firefox_jetstream2': float,
#         'macos_docker_firefox_x_jetstream2': float,
#         'macos_host_compromised_firefox_jetstream2': float,
#         'macos_docker_compromised_firefox_x_jetstream2': float,
#         'windows_host_firefox_jetstream2': float,
#         'windows_docker_firefox_wayland_jetstream2': float,
#         'windows_docker_firefox_x_jetstream2': float,
#         'windows_host_compromised_firefox_jetstream2': float,
#         'windows_docker_compromised_firefox_wayland_jetstream2': float,
#         'windows_docker_compromised_firefox_x_jetstream2': float,
#     },
#     'confidence_intervals' : {  # 95% confidence intervals
#         'linux_host_firefox_wayland_jetstream2': [113.476, 116.237]
#         'linux_docker_firefox_wayland_jetstream2': [116.826, 119.058],
#         'linux_host_compromised_firefox_wayland_jetstream2': list(float),
#         'linux_docker_compromised_firefox_wayland_jetstream2': list(float),
#         'linux_host_firefox_x_jetstream2': list(float),
#         'linux_docker_firefox_x_jetstream2': list(float),
#         'linux_host_compromised_firefox_x_jetstream2': list(float),
#         'linux_docker_compromised_firefox_x_jetstream2': list(float),
#         'macos_host_firefox_jetstream2': list(float),
#         'macos_docker_firefox_x_jetstream2': list(float),
#         'macos_host_compromised_firefox_jetstream2': list(float),
#         'macos_docker_compromised_firefox_x_jetstream2': list(float),
#         'windows_host_firefox_jetstream2': list(float),
#         'windows_docker_firefox_wayland_jetstream2': list(float),
#         'windows_docker_firefox_x_jetstream2': list(float),
#         'windows_host_compromised_firefox_jetstream2': list(float),
#         'windows_docker_compromised_firefox_wayland_jetstream2': list(float),
#         'windows_docker_compromised_firefox_x_jetstream2': list(float),
#     },
#     'means_in_confidence_intervals': {
#         'linux_host_firefox_wayland_jetstream2': True,  # 114.856 is in [113.476, 116.237]
#         'linux_docker_firefox_wayland_jetstream2': True,  # 117.942 is in [116.826, 119.058]
#         'linux_host_compromised_firefox_wayland_jetstream2': bool,
#         'linux_docker_compromised_firefox_wayland_jetstream2': bool,
#         'linux_host_firefox_x_jetstream2': bool,
#         'linux_docker_firefox_x_jetstream2': bool,
#         'linux_host_compromised_firefox_x_jetstream2': bool,
#         'linux_docker_compromised_firefox_x_jetstream2': bool,
#         'macos_host_firefox_jetstream2': bool,
#         'macos_docker_firefox_x_jetstream2': bool,
#         'macos_host_compromised_firefox_jetstream2': bool,
#         'macos_docker_compromised_firefox_x_jetstream2': bool,
#         'windows_host_firefox_jetstream2': bool,
#         'windows_docker_firefox_wayland_jetstream2': bool,
#         'windows_docker_firefox_x_jetstream2': bool,
#         'windows_host_compromised_firefox_jetstream2': bool,
#         'windows_docker_compromised_firefox_wayland_jetstream2': bool,
#         'windows_docker_compromised_firefox_x_jetstream2': bool,
#     },
#     'performance_ratios': {
#         'linux_ratio_wayland_jetstream2': 0.974  # 0.974 = 114.856/117.942 (mean_native/mean_dockerised),
#         'linux_ratio_x_jetstream2': float,
#         'macos_ratio_x_jetstream2': float,
#         'windows_ratio_wayland_jetstream2': float,
#         'windows_ratio_x_jetstream2': float,
#         'linux_ratio_compromised_wayland_jetstream2': float,
#         'linux_ratio_compromised_x_jetstream2': float,
#         'macos_ratio_compromised_x_jetstream2': float,
#         'windows_ratio_compromised_wayland_jetstream2': float,
#         'windows_ratio_compromised_x_jetstream2': float,
#     }
# }


#############################
# MotionMark data structure #
#############################

# motionmark_data = {
#     'raw_data': {  # raw data from the screenshot of a benchmark execution
#         'linux_host_firefox_wayland_motionmark': [369.28,...]  # Score
#         ],
#         'linux_docker_firefox_wayland_motionmark': [332.41,...]
#         ],
#         'linux_host_compromised_firefox_wayland_motionmark': list(float),
#         'linux_docker_compromised_firefox_wayland_motionmark': list(float),
#         'linux_host_firefox_x_motionmark': list(float),
#         'linux_docker_firefox_x_motionmark': list(float),
#         'linux_host_compromised_firefox_x_motionmark': list(float),
#         'linux_docker_compromised_firefox_x_motionmark': list(float),
#         'macos_host_firefox_motionmark': list(float),
#         'macos_docker_firefox_x_motionmark': list(float),
#         'macos_host_compromised_firefox_motionmark': list(float),
#         'macos_docker_compromised_firefox_x_motionmark': list(float),
#         'windows_host_firefox_motionmark': list(float),
#         'windows_docker_firefox_wayland_motionmark': list(float),
#         'windows_docker_firefox_x_motionmark': list(float),
#         'windows_host_compromised_firefox_motionmark': list(float),
#         'windows_docker_compromised_firefox_wayland_motionmark': list(float),
#         'windows_docker_compromised_firefox_x_motionmark': list(float),
#     },
#     'means': {  # MotionMark score value
#         'linux_host_firefox_wayland_motionmark': 369.28,
#         'linux_docker_firefox_wayland_motionmark': 332.41,
#         'linux_host_compromised_firefox_wayland_motionmark': float,
#         'linux_docker_compromised_firefox_wayland_motionmark': float,
#         'linux_host_firefox_x_motionmark': float,
#         'linux_docker_firefox_x_motionmark': float,
#         'linux_host_compromised_firefox_x_motionmark': float,
#         'linux_docker_compromised_firefox_x_motionmark': float,
#         'macos_host_firefox_motionmark': float,
#         'macos_docker_firefox_x_motionmark': float,
#         'macos_host_compromised_firefox_motionmark': float,
#         'macos_docker_compromised_firefox_x_motionmark': float,
#         'windows_host_firefox_motionmark': float,
#         'windows_docker_firefox_wayland_motionmark': float,
#         'windows_docker_firefox_x_motionmark': float,
#         'windows_host_compromised_firefox_motionmark': float,
#         'windows_docker_compromised_firefox_wayland_motionmark': float,
#         'windows_docker_compromised_firefox_x_motionmark': float,
#     },
#     'confidence_intervals' : {
#         'linux_host_firefox_wayland_motionmark': [329.66, 408.90]  # 95% confidence interval
#         'linux_docker_firefox_wayland_motionmark': list(float)
#         'linux_host_compromised_firefox_wayland_motionmark': list(float)
#         'linux_docker_compromised_firefox_wayland_motionmark': list(float)
#         'linux_host_firefox_x_motionmark': list(float)
#         'linux_docker_firefox_x_motionmark': list(float)
#         'linux_host_compromised_firefox_x_motionmark': list(float)
#         'linux_docker_compromised_firefox_x_motionmark': list(float)
#         'macos_host_firefox_motionmark': list(float)
#         'macos_docker_firefox_x_motionmark': list(float)
#         'macos_host_compromised_firefox_motionmark': list(float)
#         'macos_docker_compromised_firefox_x_motionmark': list(float)
#         'windows_host_firefox_motionmark': list(float)
#         'windows_docker_firefox_wayland_motionmark': list(float)
#         'windows_docker_firefox_x_motionmark': list(float)
#         'windows_host_compromised_firefox_motionmark': list(float)
#         'windows_docker_compromised_firefox_wayland_motionmark': list(float)
#         'windows_docker_compromised_firefox_x_motionmark': list(float)
#     },
#     'means_in_confidence_intervals': {
#         'linux_host_firefox_wayland_motionmark': True  # 369.28 is in [329.66, 408.90]
#         'linux_docker_firefox_wayland_motionmark': bool,
#         'linux_host_compromised_firefox_wayland_motionmark': bool,
#         'linux_docker_compromised_firefox_wayland_motionmark': bool,
#         'linux_host_firefox_x_motionmark': bool,
#         'linux_docker_firefox_x_motionmark': bool,
#         'linux_host_compromised_firefox_x_motionmark': bool,
#         'linux_docker_compromised_firefox_x_motionmark': bool,
#         'macos_host_firefox_motionmark': bool,
#         'macos_docker_firefox_x_motionmark': bool,
#         'macos_host_compromised_firefox_motionmark': bool,
#         'macos_docker_compromised_firefox_x_motionmark': bool,
#         'windows_host_firefox_motionmark': bool,
#         'windows_docker_firefox_wayland_motionmark': bool,
#         'windows_docker_firefox_x_motionmark': bool,
#         'windows_host_compromised_firefox_motionmark': bool,
#         'windows_docker_compromised_firefox_wayland_motionmark': bool,
#         'windows_docker_compromised_firefox_x_motionmark': bool,
#     },
#     'performance_ratios': {
#         'linux_ratio_wayland_jetstream2': 1.11  # 1.11 = 369.28/332.41 (native/dockerised),
#         'linux_ratio_x_jetstream2': float,
#         'macos_ratio_x_jetstream2': float,
#         'windows_ratio_wayland_jetstream2': float,
#         'windows_ratio_x_jetstream2': float,
#         'linux_ratio_compromised_wayland_jetstream2': float,
#         'linux_ratio_compromised_x_jetstream2': float,
#         'macos_ratio_compromised_x_jetstream2': float,
#         'windows_ratio_compromised_wayland_jetstream2': float,
#         'windows_ratio_compromised_x_jetstream2': float,
#     }
# }

##############################
# speedometer3 data structure #
##############################

# speedometer3_data = {
#     'raw_data': {  # raw data from the screenshot of a benchmark execution
#         'linux_host_firefox_wayland_speedometer3': list(float),
#         'linux_docker_firefox_wayland_speedometer3': list(float),
#         'linux_host_compromised_firefox_wayland_speedometer3': list(tuple),
#         'linux_docker_compromised_firefox_wayland_speedometer3': list(tuple),
#         'linux_host_firefox_x_speedometer3': list(tuple),
#         'linux_docker_firefox_x_speedometer3': list(tuple),
#         'linux_host_compromised_firefox_x_speedometer3': list(tuple),
#         'linux_docker_compromised_firefox_x_speedometer3': list(tuple),
#         'macos_host_firefox_speedometer3': list(tuple),
#         'macos_docker_firefox_x_speedometer3': list(tuple),
#         'macos_host_compromised_firefox_speedometer3': list(tuple),
#         'macos_docker_compromised_firefox_x_speedometer3': list(tuple),
#         'windows_host_firefox_speedometer3': list(tuple),
#         'windows_docker_firefox_wayland_speedometer3': list(tuple),
#         'windows_docker_firefox_x_speedometer3': list(tuple),
#         'windows_host_compromised_firefox_speedometer3': list(tuple),
#         'windows_docker_compromised_firefox_wayland_speedometer3': list(tuple),
#         'windows_docker_compromised_firefox_x_speedometer3': list(tuple),
#     },
#     'means': {
#         'linux_host_firefox_wayland_speedometer3': 169.6,  # mean of the 20 benchmarks (which is a grand mean)
#         'linux_docker_firefox_wayland_speedometer3': 181.0,
#         'linux_host_compromised_firefox_wayland_speedometer3': float,
#         'linux_docker_compromised_firefox_wayland_speedometer3': float,
#         'linux_host_firefox_x_speedometer3': float,
#         'linux_docker_firefox_x_speedometer3': float,
#         'linux_host_compromised_firefox_x_speedometer3': float,
#         'linux_docker_compromised_firefox_x_speedometer3': float,
#         'macos_host_firefox_speedometer3': float,
#         'macos_docker_firefox_x_speedometer3': float,
#         'macos_host_compromised_firefox_speedometer3': float,
#         'macos_docker_compromised_firefox_x_speedometer3': float,
#         'windows_host_firefox_speedometer3': float,
#         'windows_docker_firefox_wayland_speedometer3': float,
#         'windows_docker_firefox_x_speedometer3': float,
#         'windows_host_compromised_firefox_speedometer3': float,
#         'windows_docker_compromised_firefox_wayland_speedometer3': float,
#         'windows_docker_compromised_firefox_x_speedometer3': float,
#     },
#     'confidence_intervals' : {
#         'linux_host_firefox_wayland_speedometer3': [168.2, 171.0],  # speedometer3 95% confidence interval
#         'linux_docker_firefox_wayland_speedometer3': [179.5, 182.5],
#         'linux_host_compromised_firefox_wayland_speedometer3': list(float)
#         'linux_docker_compromised_firefox_wayland_speedometer3': list(float)
#         'linux_host_firefox_x_speedometer3': list(float)
#         'linux_docker_firefox_x_speedometer3': list(float)
#         'linux_host_compromised_firefox_x_speedometer3': list(float)
#         'linux_docker_compromised_firefox_x_speedometer3': list(float)
#         'macos_host_firefox_speedometer3': list(float)
#         'macos_docker_firefox_x_speedometer3': list(float)
#         'macos_host_compromised_firefox_speedometer3': list(float)
#         'macos_docker_compromised_firefox_x_speedometer3': list(float)
#         'windows_host_firefox_speedometer3': list(float)
#         'windows_docker_firefox_wayland_speedometer3': list(float)
#         'windows_docker_firefox_x_speedometer3': list(float)
#         'windows_host_compromised_firefox_speedometer3': list(float)
#         'windows_docker_compromised_firefox_wayland_speedometer3': list(float)
#         'windows_docker_compromised_firefox_x_speedometer3': list(float)
#     },
#     'means_in_confidence_intervals': {
#         'linux_host_firefox_wayland_speedometer3': True,  # 169.6 is in [168.2, 171.0]
#         'linux_docker_firefox_wayland_speedometer3': True,  # 181.0 is in [179.5, 182.5]
#         'linux_host_compromised_firefox_wayland_speedometer3': bool,
#         'linux_docker_compromised_firefox_wayland_speedometer3': bool,
#         'linux_host_firefox_x_speedometer3': bool,
#         'linux_docker_firefox_x_speedometer3': bool,
#         'linux_host_compromised_firefox_x_speedometer3': bool,
#         'linux_docker_compromised_firefox_x_speedometer3': bool,
#         'macos_host_firefox_speedometer3': bool,
#         'macos_docker_firefox_x_speedometer3': bool,
#         'macos_host_compromised_firefox_speedometer3': bool,
#         'macos_docker_compromised_firefox_x_speedometer3': bool,
#         'windows_host_firefox_speedometer3': bool,
#         'windows_docker_firefox_wayland_speedometer3': bool,
#         'windows_docker_firefox_x_speedometer3': bool,
#         'windows_host_compromised_firefox_speedometer3': bool,
#         'windows_docker_compromised_firefox_wayland_speedometer3': bool,
#         'windows_docker_compromised_firefox_x_speedometer3': bool,
#     },
#     'performance_ratios': {
#         'linux_ratio_wayland_jetstream2': 0.94  # 0.94 = 169.6/181.0 (native/dockerised),
#         'linux_ratio_x_jetstream2': float,
#         'macos_ratio_x_jetstream2': float,
#         'windows_ratio_wayland_jetstream2': float,
#         'windows_ratio_x_jetstream2': float,
#         'linux_ratio_compromised_wayland_jetstream2': float,
#         'linux_ratio_compromised_x_jetstream2': float,
#         'macos_ratio_compromised_x_jetstream2': float,
#         'windows_ratio_compromised_wayland_jetstream2': float,
#         'windows_ratio_compromised_x_jetstream2': float,
#     }
# }


######################
######################
## JetStream2 study ##
######################
######################

jetstream2_benchmarks_paths = {
    'linux_host_firefox_wayland_jetstream2': f'{DATA_BASE_DIR}/Linux (Ubuntu)/host-wayland/vanilla/jetstream2',
    'linux_docker_firefox_wayland_jetstream2': f'{DATA_BASE_DIR}/Linux (Ubuntu)/docker-wayland/vanilla/jetstream2',
    'linux_host_compromised_firefox_wayland_jetstream2': (
        f'{DATA_BASE_DIR}/Linux (Ubuntu)/host-wayland/compromised/jetstream2'
    ),
    'linux_docker_compromised_firefox_wayland_jetstream2': (
        f'{DATA_BASE_DIR}/Linux (Ubuntu)/docker-wayland/compromised/jetstream2'
    ),
    'linux_host_firefox_x_jetstream2': f'{DATA_BASE_DIR}/Linux (Ubuntu)/host-x/vanilla/jetstream2',
    'linux_docker_firefox_x_jetstream2': f'{DATA_BASE_DIR}/Linux (Ubuntu)/docker-x/vanilla/jetstream2',
    'linux_host_compromised_firefox_x_jetstream2': f'{DATA_BASE_DIR}/Linux (Ubuntu)/host-x/compromised/jetstream2',
    'linux_docker_compromised_firefox_x_jetstream2': (
        f'{DATA_BASE_DIR}/Linux (Ubuntu)/docker-x/compromised/jetstream2'
    ),
    'macos_host_firefox_jetstream2': f'{DATA_BASE_DIR}/macOS (arm64)/host/vanilla/jetstream2',
    'macos_docker_firefox_x_jetstream2': f'{DATA_BASE_DIR}/macOS (arm64)/docker-x/vanilla/jetstream2',
    'macos_host_compromised_firefox_jetstream2': f'{DATA_BASE_DIR}/macOS (arm64)/host/compromised/jetstream2',
    'macos_docker_compromised_firefox_x_jetstream2': f'{DATA_BASE_DIR}/macOS (arm64)/docker-x/compromised/jetstream2',
    'windows_host_firefox_jetstream2': f'{DATA_BASE_DIR}/Windows/host/vanilla/jetstream2',
    'windows_docker_firefox_wayland_jetstream2': f'{DATA_BASE_DIR}/Windows/docker-wayland/vanilla/jetstream2',
    'windows_docker_firefox_x_jetstream2': f'{DATA_BASE_DIR}/Windows/docker-x/vanilla/jetstream2',
    'windows_host_compromised_firefox_jetstream2': f'{DATA_BASE_DIR}/Windows/host/compromised/jetstream2',
    'windows_docker_compromised_firefox_wayland_jetstream2': (
        f'{DATA_BASE_DIR}/Windows/docker-wayland/compromised/jetstream2'
    ),
    'windows_docker_compromised_firefox_x_jetstream2': f'{DATA_BASE_DIR}/Windows/docker-x/compromised/jetstream2'
}

jetstream2_data = {
    'raw_data': {
        'linux_host_firefox_wayland_jetstream2': [],
        'linux_docker_firefox_wayland_jetstream2': [],
        'linux_host_compromised_firefox_wayland_jetstream2': [],
        'linux_docker_compromised_firefox_wayland_jetstream2': [],
        'linux_host_firefox_x_jetstream2': [],
        'linux_docker_firefox_x_jetstream2': [],
        'linux_host_compromised_firefox_x_jetstream2': [],
        'linux_docker_compromised_firefox_x_jetstream2': [],
        'macos_host_firefox_jetstream2': [],
        'macos_docker_firefox_x_jetstream2': [],
        'macos_host_compromised_firefox_jetstream2': [],
        'macos_docker_compromised_firefox_x_jetstream2': [],
        'windows_host_firefox_jetstream2': [],
        'windows_docker_firefox_wayland_jetstream2': [],
        'windows_docker_firefox_x_jetstream2': [],
        'windows_host_compromised_firefox_jetstream2': [],
        'windows_docker_compromised_firefox_wayland_jetstream2': [],
        'windows_docker_compromised_firefox_x_jetstream2': []
    },
    'means': {},
    'confidence_intervals' : {},
    'means_in_confidence_intervals': {},
    'performance_ratios': {}
}

if DEBUG:
    for configuration in jetstream2_data['raw_data']:
        print(
            "Nb of JetStream2 benchmarks: "
            f"{len(os.listdir(jetstream2_benchmarks_paths[configuration]))} - {configuration}"
        )

for configuration in jetstream2_data['raw_data']:
    for json_file in os.listdir(jetstream2_benchmarks_paths[configuration]):
        jetstream2_data['raw_data'][configuration].append(
            get_benchmark_score('jetstream2', f"{jetstream2_benchmarks_paths[configuration]}/{json_file}")
        )

for data in jetstream2_data['raw_data']:
    mean = calculate_arithmetic_mean(jetstream2_data['raw_data'][data])
    jetstream2_data['means'][data] = mean

    confidence_interval_list = confidence_interval_sample(jetstream2_data['raw_data'][data], mean, 0.95)
    jetstream2_data['confidence_intervals'][data] = confidence_interval_list

    if confidence_interval_list[0] <= mean <= confidence_interval_list[1]:
        jetstream2_data['means_in_confidence_intervals'][data] = True
    else:
        jetstream2_data['means_in_confidence_intervals'][data] = False

jetstream2_data['performance_ratios'] = {
    'linux_ratio_wayland_jetstream2': performance_ratio(
        jetstream2_data['means']['linux_host_firefox_wayland_jetstream2'],
        jetstream2_data['means']['linux_docker_firefox_wayland_jetstream2']
    ),
    'linux_ratio_x_jetstream2': performance_ratio(
        jetstream2_data['means']['linux_host_firefox_x_jetstream2'],
        jetstream2_data['means']['linux_docker_firefox_x_jetstream2']
    ),
    'macos_ratio_x_jetstream2': performance_ratio(
        jetstream2_data['means']['macos_host_firefox_jetstream2'],
        jetstream2_data['means']['macos_docker_firefox_x_jetstream2']
    ),
    'windows_ratio_wayland_jetstream2': performance_ratio(
        jetstream2_data['means']['windows_host_firefox_jetstream2'],
        jetstream2_data['means']['windows_docker_firefox_wayland_jetstream2']
    ),
    'windows_ratio_x_jetstream2': performance_ratio(
        jetstream2_data['means']['windows_host_firefox_jetstream2'],
        jetstream2_data['means']['windows_docker_firefox_x_jetstream2']
    ),
    'linux_ratio_compromised_wayland_jetstream2': performance_ratio(
        jetstream2_data['means']['linux_host_compromised_firefox_wayland_jetstream2'],
        jetstream2_data['means']['linux_docker_compromised_firefox_wayland_jetstream2']
    ),
    'linux_ratio_compromised_x_jetstream2': performance_ratio(
        jetstream2_data['means']['linux_host_compromised_firefox_x_jetstream2'],
        jetstream2_data['means']['linux_docker_compromised_firefox_x_jetstream2']
    ),
    'macos_ratio_compromised_x_jetstream2': performance_ratio(
        jetstream2_data['means']['macos_host_compromised_firefox_jetstream2'],
        jetstream2_data['means']['macos_docker_compromised_firefox_x_jetstream2']
    ),
    'windows_ratio_compromised_wayland_jetstream2': performance_ratio(
        jetstream2_data['means']['windows_host_compromised_firefox_jetstream2'],
        jetstream2_data['means']['windows_docker_compromised_firefox_wayland_jetstream2']
    ),
    'windows_ratio_compromised_x_jetstream2': performance_ratio(
        jetstream2_data['means']['windows_host_compromised_firefox_jetstream2'],
        jetstream2_data['means']['windows_docker_compromised_firefox_x_jetstream2']
    )
}


# #########################
# # JetStream2 graph data #
# #########################

jetstream2_graph_ratios_data = [
    jetstream2_data['performance_ratios']['linux_ratio_wayland_jetstream2'],
    jetstream2_data['performance_ratios']['linux_ratio_x_jetstream2'],
    jetstream2_data['performance_ratios']['macos_ratio_x_jetstream2'],
    jetstream2_data['performance_ratios']['windows_ratio_wayland_jetstream2'],
    jetstream2_data['performance_ratios']['windows_ratio_x_jetstream2'],
    jetstream2_data['performance_ratios']['linux_ratio_compromised_wayland_jetstream2'],
    jetstream2_data['performance_ratios']['linux_ratio_compromised_x_jetstream2'],
    jetstream2_data['performance_ratios']['macos_ratio_compromised_x_jetstream2'],
    jetstream2_data['performance_ratios']['windows_ratio_compromised_wayland_jetstream2'],
    jetstream2_data['performance_ratios']['windows_ratio_compromised_x_jetstream2']
]


# ######################
# ######################
# ## MotionMark study ##
# ######################
# ######################

motionmark_benchmarks_paths = {
    'linux_host_firefox_wayland_motionmark': f'{DATA_BASE_DIR}/Linux (Ubuntu)/host-wayland/vanilla/motionmark',
    'linux_docker_firefox_wayland_motionmark': f'{DATA_BASE_DIR}/Linux (Ubuntu)/docker-wayland/vanilla/motionmark',
    'linux_host_compromised_firefox_wayland_motionmark': (
        f'{DATA_BASE_DIR}/Linux (Ubuntu)/host-wayland/compromised/motionmark'
    ),
    'linux_docker_compromised_firefox_wayland_motionmark': (
        f'{DATA_BASE_DIR}/Linux (Ubuntu)/docker-wayland/compromised/motionmark'
    ),
    'linux_host_firefox_x_motionmark': f'{DATA_BASE_DIR}/Linux (Ubuntu)/host-x/vanilla/motionmark',
    'linux_docker_firefox_x_motionmark': f'{DATA_BASE_DIR}/Linux (Ubuntu)/docker-x/vanilla/motionmark',
    'linux_host_compromised_firefox_x_motionmark': f'{DATA_BASE_DIR}/Linux (Ubuntu)/host-x/compromised/motionmark',
    'linux_docker_compromised_firefox_x_motionmark': (
        f'{DATA_BASE_DIR}/Linux (Ubuntu)/docker-x/compromised/motionmark'
    ),
    'macos_host_firefox_motionmark': f'{DATA_BASE_DIR}/macOS (arm64)/host/vanilla/motionmark',
    'macos_docker_firefox_x_motionmark': f'{DATA_BASE_DIR}/macOS (arm64)/docker-x/vanilla/motionmark',
    'macos_host_compromised_firefox_motionmark': f'{DATA_BASE_DIR}/macOS (arm64)/host/compromised/motionmark',
    'macos_docker_compromised_firefox_x_motionmark': f'{DATA_BASE_DIR}/macOS (arm64)/docker-x/compromised/motionmark',
    'windows_host_firefox_motionmark': f'{DATA_BASE_DIR}/Windows/host/vanilla/motionmark',
    'windows_docker_firefox_wayland_motionmark': f'{DATA_BASE_DIR}/Windows/docker-wayland/vanilla/motionmark',
    'windows_docker_firefox_x_motionmark': f'{DATA_BASE_DIR}/Windows/docker-x/vanilla/motionmark',
    'windows_host_compromised_firefox_motionmark': f'{DATA_BASE_DIR}/Windows/host/compromised/motionmark',
    'windows_docker_compromised_firefox_wayland_motionmark': (
        f'{DATA_BASE_DIR}/Windows/docker-wayland/compromised/motionmark'
    ),
    'windows_docker_compromised_firefox_x_motionmark': f'{DATA_BASE_DIR}/Windows/docker-x/compromised/motionmark'
}

motionmark_data = {
    'raw_data': {
        'linux_host_firefox_wayland_motionmark': [],
        'linux_docker_firefox_wayland_motionmark': [],
        'linux_host_compromised_firefox_wayland_motionmark': [],
        'linux_docker_compromised_firefox_wayland_motionmark': [],
        'linux_host_firefox_x_motionmark': [],
        'linux_docker_firefox_x_motionmark': [],
        'linux_host_compromised_firefox_x_motionmark': [],
        'linux_docker_compromised_firefox_x_motionmark': [],
        'macos_host_firefox_motionmark': [],
        'macos_docker_firefox_x_motionmark': [],
        'macos_host_compromised_firefox_motionmark': [],
        'macos_docker_compromised_firefox_x_motionmark': [],
        'windows_host_firefox_motionmark': [],
        'windows_docker_firefox_wayland_motionmark': [],
        'windows_docker_firefox_x_motionmark': [],
        'windows_host_compromised_firefox_motionmark': [],
        'windows_docker_compromised_firefox_wayland_motionmark': [],
        'windows_docker_compromised_firefox_x_motionmark': []
    },
    'means': {},
    'confidence_intervals' : {},
    'means_in_confidence_intervals': {},
    'performance_ratios': {}
}

if DEBUG:
    for configuration in motionmark_data['raw_data']:
        print(
            "Nb of MotionMark benchmarks: "
            f"{len(os.listdir(motionmark_benchmarks_paths[configuration]))} - {configuration}"
        )

for configuration in motionmark_data['raw_data']:
    for json_file in os.listdir(motionmark_benchmarks_paths[configuration]):
        motionmark_data['raw_data'][configuration].append(
            get_benchmark_score('motionmark', f"{motionmark_benchmarks_paths[configuration]}/{json_file}")
        )

for data in motionmark_data['raw_data']:
    mean = calculate_arithmetic_mean(motionmark_data['raw_data'][data])
    motionmark_data['means'][data] = mean

    confidence_interval_list = confidence_interval_sample(motionmark_data['raw_data'][data], mean, 0.95)
    motionmark_data['confidence_intervals'][data] = confidence_interval_list

    if confidence_interval_list[0] <= mean <= confidence_interval_list[1]:
        motionmark_data['means_in_confidence_intervals'][data] = True
    else:
        motionmark_data['means_in_confidence_intervals'][data] = False

motionmark_data['performance_ratios'] = {
    'linux_ratio_wayland_motionmark': performance_ratio(
        motionmark_data['means']['linux_host_firefox_wayland_motionmark'],
        motionmark_data['means']['linux_docker_firefox_wayland_motionmark']
    ),
    'linux_ratio_x_motionmark': performance_ratio(
        motionmark_data['means']['linux_host_firefox_x_motionmark'],
        motionmark_data['means']['linux_docker_firefox_x_motionmark']
    ),
    'macos_ratio_x_motionmark': performance_ratio(
        motionmark_data['means']['macos_host_firefox_motionmark'],
        motionmark_data['means']['macos_docker_firefox_x_motionmark']
    ),
    'windows_ratio_wayland_motionmark': performance_ratio(
        motionmark_data['means']['windows_host_firefox_motionmark'],
        motionmark_data['means']['windows_docker_firefox_wayland_motionmark']
    ),
    'windows_ratio_x_motionmark': performance_ratio(
        motionmark_data['means']['windows_host_firefox_motionmark'],
        motionmark_data['means']['windows_docker_firefox_x_motionmark']
    ),
    'linux_ratio_compromised_wayland_motionmark': performance_ratio(
        motionmark_data['means']['linux_host_compromised_firefox_wayland_motionmark'],
        motionmark_data['means']['linux_docker_compromised_firefox_wayland_motionmark']
    ),
    'linux_ratio_compromised_x_motionmark': performance_ratio(
        motionmark_data['means']['linux_host_compromised_firefox_x_motionmark'],
        motionmark_data['means']['linux_docker_compromised_firefox_x_motionmark']
    ),
    'macos_ratio_compromised_x_motionmark': performance_ratio(
        motionmark_data['means']['macos_host_compromised_firefox_motionmark'],
        motionmark_data['means']['macos_docker_compromised_firefox_x_motionmark']
    ),
    'windows_ratio_compromised_wayland_motionmark': performance_ratio(
        motionmark_data['means']['windows_host_compromised_firefox_motionmark'],
        motionmark_data['means']['windows_docker_compromised_firefox_wayland_motionmark']
    ),
    'windows_ratio_compromised_x_motionmark': performance_ratio(
        motionmark_data['means']['windows_host_compromised_firefox_motionmark'],
        motionmark_data['means']['windows_docker_compromised_firefox_x_motionmark']
    ),
}


# #########################
# # MotionMark graph data #
# #########################

motionmark_graph_ratios_data = [
    motionmark_data['performance_ratios']['linux_ratio_wayland_motionmark'],
    motionmark_data['performance_ratios']['linux_ratio_x_motionmark'],
    motionmark_data['performance_ratios']['macos_ratio_x_motionmark'],
    motionmark_data['performance_ratios']['windows_ratio_wayland_motionmark'],
    motionmark_data['performance_ratios']['windows_ratio_x_motionmark'],
    motionmark_data['performance_ratios']['linux_ratio_compromised_wayland_motionmark'],
    motionmark_data['performance_ratios']['linux_ratio_compromised_x_motionmark'],
    motionmark_data['performance_ratios']['macos_ratio_compromised_x_motionmark'],
    motionmark_data['performance_ratios']['windows_ratio_compromised_wayland_motionmark'],
    motionmark_data['performance_ratios']['windows_ratio_compromised_x_motionmark']
]


# #######################
# #######################
# ## speedometer3 study ##
# #######################
# #######################

speedometer3_benchmarks_paths = {
    'linux_host_firefox_wayland_speedometer3': f'{DATA_BASE_DIR}/Linux (Ubuntu)/host-wayland/vanilla/speedometer3',
    'linux_docker_firefox_wayland_speedometer3': (
        f'{DATA_BASE_DIR}/Linux (Ubuntu)/docker-wayland/vanilla/speedometer3'
    ),
    'linux_host_compromised_firefox_wayland_speedometer3': (
        f'{DATA_BASE_DIR}/Linux (Ubuntu)/host-wayland/compromised/speedometer3'
    ),
    'linux_docker_compromised_firefox_wayland_speedometer3': (
        f'{DATA_BASE_DIR}/Linux (Ubuntu)/docker-wayland/compromised/speedometer3'
    ),
    'linux_host_firefox_x_speedometer3': f'{DATA_BASE_DIR}/Linux (Ubuntu)/host-x/vanilla/speedometer3',
    'linux_docker_firefox_x_speedometer3': f'{DATA_BASE_DIR}/Linux (Ubuntu)/docker-x/vanilla/speedometer3',
    'linux_host_compromised_firefox_x_speedometer3': (
        f'{DATA_BASE_DIR}/Linux (Ubuntu)/host-x/compromised/speedometer3'
    ),
    'linux_docker_compromised_firefox_x_speedometer3': (
        f'{DATA_BASE_DIR}/Linux (Ubuntu)/docker-x/compromised/speedometer3'
    ),
    'macos_host_firefox_speedometer3': f'{DATA_BASE_DIR}/macOS (arm64)/host/vanilla/speedometer3',
    'macos_docker_firefox_x_speedometer3': f'{DATA_BASE_DIR}/macOS (arm64)/docker-x/vanilla/speedometer3',
    'macos_host_compromised_firefox_speedometer3': f'{DATA_BASE_DIR}/macOS (arm64)/host/compromised/speedometer3',
    'macos_docker_compromised_firefox_x_speedometer3': (
        f'{DATA_BASE_DIR}/macOS (arm64)/docker-x/compromised/speedometer3'
        ),
    'windows_host_firefox_speedometer3': f'{DATA_BASE_DIR}/Windows/host/vanilla/speedometer3',
    'windows_docker_firefox_wayland_speedometer3': f'{DATA_BASE_DIR}/Windows/docker-wayland/vanilla/speedometer3',
    'windows_docker_firefox_x_speedometer3': f'{DATA_BASE_DIR}/Windows/docker-x/vanilla/speedometer3',
    'windows_host_compromised_firefox_speedometer3': f'{DATA_BASE_DIR}/Windows/host/compromised/speedometer3',
    'windows_docker_compromised_firefox_wayland_speedometer3': (
        f'{DATA_BASE_DIR}/Windows/docker-wayland/compromised/speedometer3'
    ),
    'windows_docker_compromised_firefox_x_speedometer3': f'{DATA_BASE_DIR}/Windows/docker-x/compromised/speedometer3'
}

speedometer3_data = {
    'raw_data': {
        'linux_host_firefox_wayland_speedometer3': [],
        'linux_docker_firefox_wayland_speedometer3': [],
        'linux_host_compromised_firefox_wayland_speedometer3': [],
        'linux_docker_compromised_firefox_wayland_speedometer3': [],
        'linux_host_firefox_x_speedometer3': [],
        'linux_docker_firefox_x_speedometer3': [],
        'linux_host_compromised_firefox_x_speedometer3': [],
        'linux_docker_compromised_firefox_x_speedometer3': [],
        'macos_host_firefox_speedometer3': [],
        'macos_docker_firefox_x_speedometer3': [],
        'macos_host_compromised_firefox_speedometer3': [],
        'macos_docker_compromised_firefox_x_speedometer3': [],
        'windows_host_firefox_speedometer3': [],
        'windows_docker_firefox_wayland_speedometer3': [],
        'windows_docker_firefox_x_speedometer3': [],
        'windows_host_compromised_firefox_speedometer3': [],
        'windows_docker_compromised_firefox_wayland_speedometer3': [],
        'windows_docker_compromised_firefox_x_speedometer3': []
    },
    'means': {},
    'confidence_intervals' : {},
    'means_in_confidence_intervals': {},
    'performance_ratios': {}
}

if DEBUG:
    for configuration in speedometer3_data['raw_data']:
        print(
            "Nb of Speedometer benchmarks: "
            f"{len(os.listdir(speedometer3_benchmarks_paths[configuration]))} - {configuration}"
        )

for configuration in speedometer3_data['raw_data']:
    for json_file in os.listdir(speedometer3_benchmarks_paths[configuration]):
        speedometer3_data['raw_data'][configuration].append(
            get_benchmark_score('speedometer3', f"{speedometer3_benchmarks_paths[configuration]}/{json_file}")
        )

for data in speedometer3_data['raw_data']:
    mean = calculate_arithmetic_mean(speedometer3_data['raw_data'][data])
    speedometer3_data['means'][data] = mean

    confidence_interval_list = confidence_interval_sample(speedometer3_data['raw_data'][data], mean, 0.95)
    speedometer3_data['confidence_intervals'][data] = confidence_interval_list

    if confidence_interval_list[0] <= mean <= confidence_interval_list[1]:
        speedometer3_data['means_in_confidence_intervals'][data] = True
    else:
        speedometer3_data['means_in_confidence_intervals'][data] = False


speedometer3_data['performance_ratios'] = {
    'linux_ratio_wayland_speedometer3': performance_ratio(
        speedometer3_data['means']['linux_host_firefox_wayland_speedometer3'],
        speedometer3_data['means']['linux_docker_firefox_wayland_speedometer3']
    ),
    'linux_ratio_x_speedometer3': performance_ratio(
        speedometer3_data['means']['linux_host_firefox_x_speedometer3'],
        speedometer3_data['means']['linux_docker_firefox_x_speedometer3']
    ),
    'macos_ratio_x_speedometer3': performance_ratio(
        speedometer3_data['means']['macos_host_firefox_speedometer3'],
        speedometer3_data['means']['macos_docker_firefox_x_speedometer3']
    ),
    'windows_ratio_wayland_speedometer3': performance_ratio(
        speedometer3_data['means']['windows_host_firefox_speedometer3'],
        speedometer3_data['means']['windows_docker_firefox_wayland_speedometer3']
    ),
    'windows_ratio_x_speedometer3': performance_ratio(
        speedometer3_data['means']['windows_host_firefox_speedometer3'],
        speedometer3_data['means']['windows_docker_firefox_x_speedometer3']
    ),
    'linux_ratio_compromised_wayland_speedometer3': performance_ratio(
        speedometer3_data['means']['linux_host_compromised_firefox_wayland_speedometer3'],
        speedometer3_data['means']['linux_docker_compromised_firefox_wayland_speedometer3']
    ),
    'linux_ratio_compromised_x_speedometer3': performance_ratio(
        speedometer3_data['means']['linux_host_compromised_firefox_x_speedometer3'],
        speedometer3_data['means']['linux_docker_compromised_firefox_x_speedometer3']
    ),
    'macos_ratio_compromised_x_speedometer3': performance_ratio(
        speedometer3_data['means']['macos_host_compromised_firefox_speedometer3'],
        speedometer3_data['means']['macos_docker_compromised_firefox_x_speedometer3']
    ),
    'windows_ratio_compromised_wayland_speedometer3': performance_ratio(
        speedometer3_data['means']['windows_host_compromised_firefox_speedometer3'],
        speedometer3_data['means']['windows_docker_compromised_firefox_wayland_speedometer3']
    ),
    'windows_ratio_compromised_x_speedometer3': performance_ratio(
        speedometer3_data['means']['windows_host_compromised_firefox_speedometer3'],
        speedometer3_data['means']['windows_docker_compromised_firefox_x_speedometer3']
    ),
}


# ##########################
# # speedometer3 graph data #
# ##########################

speedometer3_graph_ratios_data = [
    speedometer3_data['performance_ratios']['linux_ratio_wayland_speedometer3'],
    speedometer3_data['performance_ratios']['linux_ratio_x_speedometer3'],
    speedometer3_data['performance_ratios']['macos_ratio_x_speedometer3'],
    speedometer3_data['performance_ratios']['windows_ratio_wayland_speedometer3'],
    speedometer3_data['performance_ratios']['windows_ratio_x_speedometer3'],
    speedometer3_data['performance_ratios']['linux_ratio_compromised_wayland_speedometer3'],
    speedometer3_data['performance_ratios']['linux_ratio_compromised_x_speedometer3'],
    speedometer3_data['performance_ratios']['macos_ratio_compromised_x_speedometer3'],
    speedometer3_data['performance_ratios']['windows_ratio_compromised_wayland_speedometer3'],
    speedometer3_data['performance_ratios']['windows_ratio_compromised_x_speedometer3']
]

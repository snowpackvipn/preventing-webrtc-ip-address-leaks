#!/usr/bin/python3
# coding: utf-8
#
# Benchmark graphs
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

"""Matplotlib benchmark graphs

This module displays in graph form
 - the average scores of the JetStream2.3, MotionMark1.3 and Speedometer3.0 benchmarks with their associated confidence
   intervals.
 - the ratios of the average native scores to the scores of the containerised solution.
"""

__author__ = "Guillaume Nibert"
__credits__ = ["Sébastien Tixeuil", "Baptiste Polvé", "Nana J. Bakalafoua M'boussi", "Xuan Son Nguyen"]
__license__ = "GNU GPLv3"
__maintainer__ = "Guillaume Nibert"
__email__ = "guillaume.nibert@snowpack.eu"

import numpy as np
import matplotlib.pyplot as plt

import benchmark_data


def add_labels(ax: plt.subplot, x: list, y: list, score_label: str, position: str, color: str):
    """Add a label in the plt.subplot graph.

    Args:
        ax (plt.subplot): selected matplotlib subplot.
        x (list): list of x values.
        y (list | np.array): list or np.array of y values.
        score_label (str): precision (half-precision, double-precision...) (e.g. "%.2f").
        position (str): 'left' | 'right' | 'center'.
        color (str): color of the label.
    """
    for i in range(len(x)):
        ax.text(i, y[i]+0.02, score_label % y[i], ha = position, color=color)


def add_labels_bottom(ax: plt.subplot, x: list, y: list, score_label: str, margin: int, color: str='green'):
    """Add a label in the plt.subplot graph.

    Args:
        ax (plt.subplot): selected matplotlib subplot.
        x (list): list of x values.
        y (list | np.array): list or np.array of y values.
        score_label (str): precision (half-precision, double-precision...) (e.g. "%.2f").
        margin (int): Bottom margin from y-centre of the label.
        color (str, optional): color of the label. Defaults to 'green'.
    """
    for i in range(len(x)):
        ax.text(i, y[i]-margin, score_label % y[i], ha = 'center', color=color)


def add_labels_top(ax: plt.subplot, x: list, y: list, score_label: str, margin: int, color: str='green'):
    """Add a label in the plt.subplot graph.

    Args:
        ax (plt.subplot): selected matplotlib subplot.
        x (list): list of x values.
        y (list | np.array): list or np.array of y values.
        score_label (str): precision (half-precision, double-precision...) (e.g. "%.2f").
        margin (int): Top margin from y-centre of the label.
        color (str, optional): color of the label. Defaults to 'green'.
    """
    for i in range(len(x)):
        ax.text(i, y[i]+margin, score_label % y[i], ha = 'center', color=color)


def means_confidence_intervals_plot(means: list,
                                    confidence_interval_list: list,
                                    title: str,
                                    label_score: str,
                                    label_ci: str,
                                    ylabel: str,
                                    score_label: str,
                                    margin_label: int):
    """Plot the mean scores with their associated confidence intervals for a given benchmark.

    Args:
        means (list): Mean benchmark scores by configuration tested.
        confidence_interval_list (list): Confidence intervals associated with each mean score.
        title (str): Title of the graph.
        label_score (str): Label title representing mean scores.
        label_ci (str): Label title representing associated confidence intervals.
        ylabel (str): Y label title (i.e. "Benchmark score").
        score_label (str): precision (half-precision, double-precision...) of the mean score displayed (e.g. "%.2f").
        margin_label (int): margin from y-centre of the score label.
    """
    configs = [
        'LNVW',  # Linux Native Vanilla Wayland
        'LNCW',  # Linux Native Compromised Wayland
        'LNVX',  # Linux Native Vanilla X
        'LNCX',  # Linux Native Compromised X
        'MNV',   # macOS Native Vanilla
        'MNC',   # macOS Native Compromised
        'WNV',   # Windows Native Vanilla
        'WNC',   # Windows Native Compromised
        'LDVW',  # Linux Dockerised Vanilla Wayland
        'LDCW',  # Linux Dockerised Compromised Wayland
        'LDVX',  # Linux Dockerised Vanilla X
        'LDCX',  # Linux Dockerised Compromised X
        'MDV',   # macOS Dockerised Vanilla
        'MDC',   # macOS Dockerised Compromised
        'WDVW',  # Windows Dockerised Vanilla Wayland
        'WDCW',  # Windows Dockerised Compromised Wayland
        'WDVX',  # Windows Dockerised Vanilla X
        'WDCX'   # Windows Dockerised Compromised X
    ]

    confidence_interval_array = np.array(confidence_interval_list)

    _unused_fig, ax = plt.subplots()

    ax.plot(configs, means, color="red", linewidth=1, label=label_score)
    ax.fill_between(configs,
                    confidence_interval_array[:, 0],
                    confidence_interval_array[:, 1],
                    alpha=0.2,
                    color="green",
                    label=label_ci)

    add_labels(ax, configs, means, score_label, 'center', 'red')
    add_labels_bottom(ax, configs, confidence_interval_array[:, 0], score_label, margin_label)
    add_labels_top(ax, configs, confidence_interval_array[:, 1], score_label, margin_label)

    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend()

    plt.tight_layout()
    plt.subplots_adjust(bottom=0.25)

    plt.show()


def ratios_plot(ratio_values: list,
                title: str,
                ylabel: str,
                score_label: str):
    """Plot the ratios (native solution to container) for each comparable configuration tested.

    Args:
        ratio_values (list): List of ratios (native solution to container) for each comparable configuration tested.
        title (str): Title of the graph.
        ylabel (str): Y label title (i.e. "Ratio").
        score_label (str): precision (half-precision, double-precision...) of the mean score displayed (e.g. "%.2f").
    """

    ratios = [
        'Linux Wayland',
        'Linux X',
        'macOS',
        'Windows Wayland',
        'Windows X'
    ]

    _unused_fig, ax = plt.subplots()

    x_axis = np.arange(len(ratios))

    ax.bar(x_axis - 0.2, ratio_values[:5], 0.4, color="blue", label="Vanilla Firefox")
    ax.bar(x_axis + 0.2, ratio_values[5:], 0.4, color="red", label="Compromised Firefox")

    add_labels(ax, ratios, ratio_values[:5], score_label, 'right', 'blue')
    add_labels(ax, ratios, ratio_values[5:], score_label, 'left', 'red')

    ax.set_xticks(x_axis)
    ax.set_xticklabels(ratios)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend()

    plt.tight_layout()
    plt.subplots_adjust(bottom=0.45)

    plt.show()


if __name__== "__main__":

    pgfplot_mean_configs = [
        'LNVW    ',  # Linux Native Vanilla Wayland
        'LNCW    ',  # Linux Native Compromised Wayland
        'LNVX    ',  # Linux Native Vanilla X
        'LNCX    ',  # Linux Native Compromised X
        'MNV     ',  # macOS Native Vanilla
        'MNC     ',  # macOS Native Compromised
        'WNV     ',  # Windows Native Vanilla
        'WNC     ',  # Windows Native Compromised
        'LDVW    ',  # Linux Dockerised Vanilla Wayland
        'LDCW    ',  # Linux Dockerised Compromised Wayland
        'LDVX    ',  # Linux Dockerised Vanilla X
        'LDCX    ',  # Linux Dockerised Compromised X
        'MDVX    ',  # macOS Dockerised Vanilla X
        'MDCX    ',  # macOS Dockerised Compromised X
        'WDVW    ',  # Windows Dockerised Vanilla Wayland
        'WDCW    ',  # Windows Dockerised Compromised Wayland
        'WDVX    ',  # Windows Dockerised Vanilla X
        'WDCX    '   # Windows Dockerised Compromised X
    ]

    pgfplot_ratio_configs = [
        'Linux Wayland    ',
        'Linux X          ',
        'macOS            ',
        'Windows Wayland  ',
        'Windows X        '
    ]

    confidence_list = []

    for configuration in benchmark_data.jetstream2_data['confidence_intervals']:
        confidence_list.append(benchmark_data.jetstream2_data['means_in_confidence_intervals'][configuration])

    for configuration in benchmark_data.motionmark_data['confidence_intervals']:
        confidence_list.append(benchmark_data.motionmark_data['means_in_confidence_intervals'][configuration])

    for configuration in benchmark_data.speedometer3_data['confidence_intervals']:
        confidence_list.append(benchmark_data.speedometer3_data['means_in_confidence_intervals'][configuration])

    print("Each mean score is in its associated confidence interval:", all(confidence_list))

    jetstream2_means_for_graph = [
        benchmark_data.jetstream2_data['means']['linux_host_firefox_wayland_jetstream2'],
        benchmark_data.jetstream2_data['means']['linux_host_compromised_firefox_wayland_jetstream2'],
        benchmark_data.jetstream2_data['means']['linux_host_firefox_x_jetstream2'],
        benchmark_data.jetstream2_data['means']['linux_host_compromised_firefox_x_jetstream2'],
        benchmark_data.jetstream2_data['means']['macos_host_firefox_jetstream2'],
        benchmark_data.jetstream2_data['means']['macos_host_compromised_firefox_jetstream2'],
        benchmark_data.jetstream2_data['means']['windows_host_firefox_jetstream2'],
        benchmark_data.jetstream2_data['means']['windows_host_compromised_firefox_jetstream2'],
        benchmark_data.jetstream2_data['means']['linux_docker_firefox_wayland_jetstream2'],
        benchmark_data.jetstream2_data['means']['linux_docker_compromised_firefox_wayland_jetstream2'],
        benchmark_data.jetstream2_data['means']['linux_docker_firefox_x_jetstream2'],
        benchmark_data.jetstream2_data['means']['linux_docker_compromised_firefox_x_jetstream2'],
        benchmark_data.jetstream2_data['means']['macos_docker_firefox_x_jetstream2'],
        benchmark_data.jetstream2_data['means']['macos_docker_compromised_firefox_x_jetstream2'],
        benchmark_data.jetstream2_data['means']['windows_docker_firefox_wayland_jetstream2'],
        benchmark_data.jetstream2_data['means']['windows_docker_compromised_firefox_wayland_jetstream2'],
        benchmark_data.jetstream2_data['means']['windows_docker_firefox_x_jetstream2'],
        benchmark_data.jetstream2_data['means']['windows_docker_compromised_firefox_x_jetstream2']
    ]


    jetstream2_confidence_intervals_for_graph = [
        benchmark_data.jetstream2_data['confidence_intervals']['linux_host_firefox_wayland_jetstream2'],
        benchmark_data.jetstream2_data['confidence_intervals']['linux_host_compromised_firefox_wayland_jetstream2'],
        benchmark_data.jetstream2_data['confidence_intervals']['linux_host_firefox_x_jetstream2'],
        benchmark_data.jetstream2_data['confidence_intervals']['linux_host_compromised_firefox_x_jetstream2'],
        benchmark_data.jetstream2_data['confidence_intervals']['macos_host_firefox_jetstream2'],
        benchmark_data.jetstream2_data['confidence_intervals']['macos_host_compromised_firefox_jetstream2'],
        benchmark_data.jetstream2_data['confidence_intervals']['windows_host_firefox_jetstream2'],
        benchmark_data.jetstream2_data['confidence_intervals']['windows_host_compromised_firefox_jetstream2'],
        benchmark_data.jetstream2_data['confidence_intervals']['linux_docker_firefox_wayland_jetstream2'],
        benchmark_data.jetstream2_data['confidence_intervals']['linux_docker_compromised_firefox_wayland_jetstream2'],
        benchmark_data.jetstream2_data['confidence_intervals']['linux_docker_firefox_x_jetstream2'],
        benchmark_data.jetstream2_data['confidence_intervals']['linux_docker_compromised_firefox_x_jetstream2'],
        benchmark_data.jetstream2_data['confidence_intervals']['macos_docker_firefox_x_jetstream2'],
        benchmark_data.jetstream2_data['confidence_intervals']['macos_docker_compromised_firefox_x_jetstream2'],
        benchmark_data.jetstream2_data['confidence_intervals']['windows_docker_firefox_wayland_jetstream2'],
        benchmark_data.jetstream2_data['confidence_intervals']['windows_docker_compromised_firefox_wayland_jetstream2'],
        benchmark_data.jetstream2_data['confidence_intervals']['windows_docker_firefox_x_jetstream2'],
        benchmark_data.jetstream2_data['confidence_intervals']['windows_docker_compromised_firefox_x_jetstream2']
    ]


    motionmark_means_for_graph = [
        benchmark_data.motionmark_data['means']['linux_host_firefox_wayland_motionmark'],
        benchmark_data.motionmark_data['means']['linux_host_compromised_firefox_wayland_motionmark'],
        benchmark_data.motionmark_data['means']['linux_host_firefox_x_motionmark'],
        benchmark_data.motionmark_data['means']['linux_host_compromised_firefox_x_motionmark'],
        benchmark_data.motionmark_data['means']['macos_host_firefox_motionmark'],
        benchmark_data.motionmark_data['means']['macos_host_compromised_firefox_motionmark'],
        benchmark_data.motionmark_data['means']['windows_host_firefox_motionmark'],
        benchmark_data.motionmark_data['means']['windows_host_compromised_firefox_motionmark'],
        benchmark_data.motionmark_data['means']['linux_docker_firefox_wayland_motionmark'],
        benchmark_data.motionmark_data['means']['linux_docker_compromised_firefox_wayland_motionmark'],
        benchmark_data.motionmark_data['means']['linux_docker_firefox_x_motionmark'],
        benchmark_data.motionmark_data['means']['linux_docker_compromised_firefox_x_motionmark'],
        benchmark_data.motionmark_data['means']['macos_docker_firefox_x_motionmark'],
        benchmark_data.motionmark_data['means']['macos_docker_compromised_firefox_x_motionmark'],
        benchmark_data.motionmark_data['means']['windows_docker_firefox_wayland_motionmark'],
        benchmark_data.motionmark_data['means']['windows_docker_compromised_firefox_wayland_motionmark'],
        benchmark_data.motionmark_data['means']['windows_docker_firefox_x_motionmark'],
        benchmark_data.motionmark_data['means']['windows_docker_compromised_firefox_x_motionmark']
    ]

    motionmark_confidence_intervals_for_graph = [
        benchmark_data.motionmark_data['confidence_intervals']['linux_host_firefox_wayland_motionmark'],
        benchmark_data.motionmark_data['confidence_intervals']['linux_host_compromised_firefox_wayland_motionmark'],
        benchmark_data.motionmark_data['confidence_intervals']['linux_host_firefox_x_motionmark'],
        benchmark_data.motionmark_data['confidence_intervals']['linux_host_compromised_firefox_x_motionmark'],
        benchmark_data.motionmark_data['confidence_intervals']['macos_host_firefox_motionmark'],
        benchmark_data.motionmark_data['confidence_intervals']['macos_host_compromised_firefox_motionmark'],
        benchmark_data.motionmark_data['confidence_intervals']['windows_host_firefox_motionmark'],
        benchmark_data.motionmark_data['confidence_intervals']['windows_host_compromised_firefox_motionmark'],
        benchmark_data.motionmark_data['confidence_intervals']['linux_docker_firefox_wayland_motionmark'],
        benchmark_data.motionmark_data['confidence_intervals']['linux_docker_compromised_firefox_wayland_motionmark'],
        benchmark_data.motionmark_data['confidence_intervals']['linux_docker_firefox_x_motionmark'],
        benchmark_data.motionmark_data['confidence_intervals']['linux_docker_compromised_firefox_x_motionmark'],
        benchmark_data.motionmark_data['confidence_intervals']['macos_docker_firefox_x_motionmark'],
        benchmark_data.motionmark_data['confidence_intervals']['macos_docker_compromised_firefox_x_motionmark'],
        benchmark_data.motionmark_data['confidence_intervals']['windows_docker_firefox_wayland_motionmark'],
        benchmark_data.motionmark_data['confidence_intervals']['windows_docker_compromised_firefox_wayland_motionmark'],
        benchmark_data.motionmark_data['confidence_intervals']['windows_docker_firefox_x_motionmark'],
        benchmark_data.motionmark_data['confidence_intervals']['windows_docker_compromised_firefox_x_motionmark']
    ]


    speedometer3_means_for_graph = [
        benchmark_data.speedometer3_data['means']['linux_host_firefox_wayland_speedometer3'],
        benchmark_data.speedometer3_data['means']['linux_host_compromised_firefox_wayland_speedometer3'],
        benchmark_data.speedometer3_data['means']['linux_host_firefox_x_speedometer3'],
        benchmark_data.speedometer3_data['means']['linux_host_compromised_firefox_x_speedometer3'],
        benchmark_data.speedometer3_data['means']['macos_host_firefox_speedometer3'],
        benchmark_data.speedometer3_data['means']['macos_host_compromised_firefox_speedometer3'],
        benchmark_data.speedometer3_data['means']['windows_host_firefox_speedometer3'],
        benchmark_data.speedometer3_data['means']['windows_host_compromised_firefox_speedometer3'],
        benchmark_data.speedometer3_data['means']['linux_docker_firefox_wayland_speedometer3'],
        benchmark_data.speedometer3_data['means']['linux_docker_compromised_firefox_wayland_speedometer3'],
        benchmark_data.speedometer3_data['means']['linux_docker_firefox_x_speedometer3'],
        benchmark_data.speedometer3_data['means']['linux_docker_compromised_firefox_x_speedometer3'],
        benchmark_data.speedometer3_data['means']['macos_docker_firefox_x_speedometer3'],
        benchmark_data.speedometer3_data['means']['macos_docker_compromised_firefox_x_speedometer3'],
        benchmark_data.speedometer3_data['means']['windows_docker_firefox_wayland_speedometer3'],
        benchmark_data.speedometer3_data['means']['windows_docker_compromised_firefox_wayland_speedometer3'],
        benchmark_data.speedometer3_data['means']['windows_docker_firefox_x_speedometer3'],
        benchmark_data.speedometer3_data['means']['windows_docker_compromised_firefox_x_speedometer3']
    ]


    speedometer3_confidence_intervals_for_graph = [
        benchmark_data.speedometer3_data['confidence_intervals']['linux_host_firefox_wayland_speedometer3'],
        benchmark_data.speedometer3_data['confidence_intervals']['linux_host_compromised_firefox_wayland_speedometer3'],
        benchmark_data.speedometer3_data['confidence_intervals']['linux_host_firefox_x_speedometer3'],
        benchmark_data.speedometer3_data['confidence_intervals']['linux_host_compromised_firefox_x_speedometer3'],
        benchmark_data.speedometer3_data['confidence_intervals']['macos_host_firefox_speedometer3'],
        benchmark_data.speedometer3_data['confidence_intervals']['macos_host_compromised_firefox_speedometer3'],
        benchmark_data.speedometer3_data['confidence_intervals']['windows_host_firefox_speedometer3'],
        benchmark_data.speedometer3_data['confidence_intervals']['windows_host_compromised_firefox_speedometer3'],
        benchmark_data.speedometer3_data['confidence_intervals']['linux_docker_firefox_wayland_speedometer3'],
        benchmark_data.speedometer3_data['confidence_intervals']['linux_docker_compromised_firefox_wayland_speedometer3'],
        benchmark_data.speedometer3_data['confidence_intervals']['linux_docker_firefox_x_speedometer3'],
        benchmark_data.speedometer3_data['confidence_intervals']['linux_docker_compromised_firefox_x_speedometer3'],
        benchmark_data.speedometer3_data['confidence_intervals']['macos_docker_firefox_x_speedometer3'],
        benchmark_data.speedometer3_data['confidence_intervals']['macos_docker_compromised_firefox_x_speedometer3'],
        benchmark_data.speedometer3_data['confidence_intervals']['windows_docker_firefox_wayland_speedometer3'],
        benchmark_data.speedometer3_data['confidence_intervals'][
            'windows_docker_compromised_firefox_wayland_speedometer3'
        ],
        benchmark_data.speedometer3_data['confidence_intervals']['windows_docker_firefox_x_speedometer3'],
        benchmark_data.speedometer3_data['confidence_intervals']['windows_docker_compromised_firefox_x_speedometer3']
    ]


    # Plot JetStream2 mean scores and associated confidence intervals graph
    means_confidence_intervals_plot(
        jetstream2_means_for_graph,
        jetstream2_confidence_intervals_for_graph,
        ("Arithmetic means of 20 JetStream2 scores and associated 95% confidence intervals for the 18 configurations "
        "tested"),
        "JetStream2 arithmetic mean score per configuration",
        "95% confidence interval",
        "JetStream2 score",
        "%.3f",
        3.5
    )

    print("\npgftable JetStream2 means:\n")

    for i in range(18):
        print(
            f"{pgfplot_mean_configs[i]} & "
            f"{jetstream2_means_for_graph[i]:.3f} & "
            f"{jetstream2_confidence_intervals_for_graph[i][0]:.3f} & "
            f"{jetstream2_confidence_intervals_for_graph[i][1]:.3f} \\\\"
        )


    # Plot MotionMark mean scores and associated confidence intervals graph
    means_confidence_intervals_plot(
        motionmark_means_for_graph,
        motionmark_confidence_intervals_for_graph,
        "Arithmetic means of 20 MotionMark scores and associated 95% confidence intervals for the 18 configurations tested",
        "MotionMark score per configuration",
        "95% confidence interval",
        "MotionMark score",
        "%.2f",
        50
    )


    print("\npgftable MotionMark means:\n")

    for i in range(18):
        print(
            f"{pgfplot_mean_configs[i]} & "
            f"{motionmark_means_for_graph[i]:.3f} & "
            f"{motionmark_confidence_intervals_for_graph[i][0]:.3f} & "
            f"{motionmark_confidence_intervals_for_graph[i][1]:.3f} \\\\"
        )


    # Plot speedometer3 mean scores and associated confidence intervals graph
    means_confidence_intervals_plot(
        speedometer3_means_for_graph,
        speedometer3_confidence_intervals_for_graph,
        ("Arithmetic means of 20 Speedometer3 scores and associated 95% confidence intervals for the 18 configurations "
        "tested"),
        "speedometer3 arithmetic mean score per configuration",
        "95% confidence interval",
        "speedometer3 score",
        "%.2f",
        0.5
    )


    print("\npgftable Speedometer means:\n")

    for i in range(18):
        print(
            f"{pgfplot_mean_configs[i]} & "
            f"{speedometer3_means_for_graph[i]:.3f} & "
            f"{speedometer3_confidence_intervals_for_graph[i][0]:.3f} & "
            f"{speedometer3_confidence_intervals_for_graph[i][1]:.3f} \\\\"
        )


    # Plot JetSream2 ratios graph
    ratios_plot(
        benchmark_data.jetstream2_graph_ratios_data,
        ("Ratios of JetStream2 mean scores for Firefox running natively compared with those for Firefox running in a "
        "container"),
        "Ratio",
        "%.2f"
    )

    print("\npgftable JetStream2 ratios:\n")

    for i in range(5):
        print(
            f"{pgfplot_ratio_configs[i]} & "
            f"{benchmark_data.jetstream2_graph_ratios_data[i]:.2f} & "
            f"{benchmark_data.jetstream2_graph_ratios_data[i+5]:.2f} \\\\"
        )


    # Plot MotionMark ratios graph
    ratios_plot(
        benchmark_data.motionmark_graph_ratios_data,
        ("Ratios of MotionMark scores for Firefox running natively compared with those for Firefox running in a "
        "container"),
        "Ratio",
        "%.2f"
    )

    print("\npgftable MotionMark ratios:\n")

    for i in range(5):
        print(
            f"{pgfplot_ratio_configs[i]} & "
            f"{benchmark_data.motionmark_graph_ratios_data[i]:.2f} & "
            f"{benchmark_data.motionmark_graph_ratios_data[i+5]:.2f} \\\\"
        )

    # Plot speedometer3 ratios graph
    ratios_plot(
        benchmark_data.speedometer3_graph_ratios_data,
        ("Ratios of Speedometer3 mean scores for Firefox running natively compared with those for Firefox running in a "
        "container"),
        "Ratio",
        "%.2f"
    )

    print("\npgftable Speedometer ratios:\n")

    for i in range(5):
        print(
            f"{pgfplot_ratio_configs[i]} & "
            f"{benchmark_data.speedometer3_graph_ratios_data[i]:.2f} & "
            f"{benchmark_data.speedometer3_graph_ratios_data[i+5]:.2f} \\\\"
        )

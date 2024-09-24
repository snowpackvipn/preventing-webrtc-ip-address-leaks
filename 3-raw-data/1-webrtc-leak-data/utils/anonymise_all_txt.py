#!/usr/bin/python3
# coding: utf-8
#
# Anonymise all txt files
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

"""Anonymise TXT files

This module contains functions for anonymising txt files with IP addresses anonymised according to RFCs 5737 and 3849.
"""

__author__ = "Guillaume Nibert"
__credits__ = ["Sébastien Tixeuil", "Baptiste Polvé", "Nana J. Bakalafoua M'boussi", "Xuan Son Nguyen"]
__license__ = "GNU GPLv3"
__maintainer__ = "Guillaume Nibert"
__email__ = "guillaume.nibert@snowpack.eu"

import os

from constants import MAC_ADRESSES, IPV4_ADDRESSES, IPV6_ADDRESSES, FQDN_ADDRESSES


def parse_and_replace_values(filename, values_to_replace):
    """Parses a text file, replaces specified values, and saves the changes.

    Args:
        filename (str): The path to the text file to be parsed.
        values_to_replace (dict): A dictionary mapping the values to be replaced
            to their corresponding replacements.
    """

    print(filename)

    with open(filename, "r", encoding="utf8") as file:
        content = file.readlines()

    with open(filename, "w", encoding="utf8") as file:
        for line in content:
            for value, replacement in values_to_replace.items():
                line = line.replace(value, replacement)
            file.write(line)

def walk_and_replace(directory, values_to_replace):
    """Walks through a directory and recursively applies `parse_and_replace_values` to all .txt files.

    Args:
        directory (str): The path to the directory to start searching from.
        values_to_replace (dict): A dictionary mapping the values to be replaced
            to their corresponding replacements.
    """

    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".txt"):
                filepath = os.path.join(root, filename)
                parse_and_replace_values(filepath, values_to_replace)


if __name__ == "__main__":

    VALUES_TO_REPLACE = {**MAC_ADRESSES, **IPV4_ADDRESSES, **IPV6_ADDRESSES, **FQDN_ADDRESSES}

    DIRECTORY = os.path.abspath(os.path.join(os.getcwd(), os.pardir))  # Path to 1-webrtc-leak-data

    walk_and_replace(DIRECTORY, VALUES_TO_REPLACE)

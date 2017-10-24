#!/usr/bin/env python
#
# Author:   Daniela Duricekova <daniela.duricekova@gmail.com>
#

"""Representation and parsing of configuration files."""

import configparser
import os


def parse_config_files(*config_files):
    config = configparser.ConfigParser()
    config.read(config_files)
    return config


def parse_our_config_files():
    config_files = [
        'config.ini',
        'config_local.ini',
    ]
    if 'TEENY_WEENY_LINK_TESTS' in os.environ:
        config_files.append('config_tests.ini')

    root_dir = os.path.join(os.path.dirname(__file__), os.pardir)
    config_files = [os.path.join(root_dir, file) for file in config_files]
    config_files = [file for file in config_files if os.path.isfile(file)]

    return parse_config_files(*config_files)

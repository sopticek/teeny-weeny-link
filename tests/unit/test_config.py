#!/usr/bin/env python
#
# Author:   Daniela Duricekova <daniela.duricekova@gmail.com>
#

"""Unit tests for the config module."""

import unittest

from teeny_weeny_link.config import parse_config_files
from teeny_weeny_link.config import parse_our_config_files
from tests.utils import TemporaryFile


class TestParseConfigFiles(unittest.TestCase):
    def test_if_no_files_are_given_empty_config_is_returned(self):
        parsed_config = parse_config_files()

        self.assertEqual(parsed_config.sections(), [])

    def test_simple_file_is_parsed_correctly(self):
        config_content = '''
        ; Local configuration file for teeny-weeny-link.
        [db]
        uri = localhost:6379

        [id_generator]
        salt = f97a41350d30ce18a4f7593123e648862bf57749
        '''

        with TemporaryFile(config_content) as cf:
            parsed_config = parse_config_files(cf.name)
            self.assertEqual(
                parsed_config.sections(),
                ['db', 'id_generator']
            )
            self.assertEqual(
                parsed_config['db']['uri'],
                'localhost:6379'
            )
            self.assertEqual(
                parsed_config['id_generator']['salt'],
                'f97a41350d30ce18a4f7593123e648862bf57749'
            )

    def test_two_files_are_parsed_correctly(self):
        global_config_content = '''
        ; Global configuration file for teeny-weeny-link.
        [db]
        uri = localhost:6379

        [id_generator]
        salt = f97a41350d30ce18a4f7593123e648862bf57749
        '''
        local_config_content = '''
        ; Local configuration file for teeny-weeny-link.
        [db]
        uri = myserver.com:6379
        '''

        with TemporaryFile(global_config_content) as global_cf:
            with TemporaryFile(local_config_content) as local_cf:
                parsed_config = parse_config_files(
                    global_cf.name,
                    local_cf.name
                )
                self.assertEqual(
                    parsed_config.sections(),
                    ['db', 'id_generator']
                )
                self.assertEqual(
                    parsed_config['db']['uri'],
                    'myserver.com:6379'
                )
                self.assertEqual(
                    parsed_config['id_generator']['salt'],
                    'f97a41350d30ce18a4f7593123e648862bf57749'
                )


class TestParseOurConfigFiles(unittest.TestCase):
    def test_config_contains_all_required_information(self):
        parsed_config = parse_our_config_files()

        self.assertIn('uri', parsed_config['db'])
        self.assertIn('salt', parsed_config['id_generator'])

#!/usr/bin/env python
#
# Author:   Daniela Duricekova <daniela.duricekova@gmail.com>
#

"""Tests for the db module."""

import unittest

from teeny_weeny_link.db import Database
from teeny_weeny_link.id_generator import IDGenerator


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db = Database(IDGenerator('0123456789'))
        self.db.remove_all_links()

    def tearDown(self):
        self.db.remove_all_links()

    def test_insert_link_inserts_link_into_database(self):
        link = 'www.google.com'

        id = self.db.insert_link(link)

        self.assertEqual(self.db.lookup_link(id), link)

    def test_insert_link_returns_different_id_for_each_link(self):
        id1 = self.db.insert_link('www.google.com')
        id2 = self.db.insert_link('www.google.co.uk')

        self.assertNotEqual(id1, id2)

    def test_visit_link_returns_original_link_for_given_id(self):
        link = 'www.google.com'

        id = self.db.insert_link(link)

        self.assertEqual(self.db.visit_link(id), link)

    def test_visit_link_increases_visit_count_in_each_call(self):
        id = self.db.insert_link('www.google.com')

        self.db.visit_link(id)
        self.db.visit_link(id)

        self.assertEqual(self.db.get_visit_count(id), 2)

    def test_visit_link_returns_none_for_nonexisting_id(self):
        id = 'xF3kx'

        link = self.db.visit_link(id)

        self.assertIsNone(link)
        self.assertIsNone(self.db.get_visit_count(id))

    def test_delete_link_deletes_link(self):
        link = 'www.google.com'
        id = self.db.insert_link(link)

        self.db.delete_link(id)

        self.assertIsNone(self.db.lookup_link(id))
        self.assertIsNone(self.db.get_visit_count(id))

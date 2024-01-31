#!/usr/bin/env python
#
# Author:   Daniela Ďuričeková <daniela.duricekova@protonmail.com>
#

"""Tests for the id_generator module."""

import unittest

from teeny_weeny_link.id_generator import IDGenerator


class TestIDGenerator(unittest.TestCase):
    def test_generator_returns_same_ids_for_same_input(self):
        g = IDGenerator('0123456789')

        self.assertEqual(g.to_id(1), g.to_id(1))

    def test_generator_returns_different_ids_for_different_input(self):
        g = IDGenerator('0123456789')

        self.assertNotEqual(g.to_id(1), g.to_id(2))

    def test_different_generators_return_different_ids_for_same_input(self):
        g1 = IDGenerator('0123456789')
        g2 = IDGenerator('9876543210')

        self.assertNotEqual(g1.to_id(1), g2.to_id(1))

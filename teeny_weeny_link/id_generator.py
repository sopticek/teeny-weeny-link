#!/usr/bin/env python
#
# Author:   Daniela Ďuričeková <daniela.duricekova@protonmail.com>
#

"""Generates IDs."""

import hashids


class IDGenerator:
    def __init__(self, salt):
        self._generator = hashids.Hashids(salt=salt)

    def to_id(self, num):
        return self._generator.encode(num)

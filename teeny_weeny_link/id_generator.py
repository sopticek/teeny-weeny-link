#!/usr/bin/env python
#
# Author:   Daniela Duricekova <daniela.duricekova@gmail.com>
#

"""Generates IDs."""

import hashids


class IDGenerator:
    def __init__(self, seed):
        self._generator = hashids.Hashids(salt=seed)

    def to_id(self, num):
        return self._generator.encode(num)

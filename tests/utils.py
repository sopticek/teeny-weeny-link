#!/usr/bin/env python
#
# Author:   Daniela Ďuričeková <daniela.duricekova@protonmail.com>
#

"""Test utilities."""

import os
from tempfile import NamedTemporaryFile


class TemporaryFile:
    def __init__(self, content):
        self.content = content

    def __enter__(self):
        with NamedTemporaryFile('wt', delete=False) as f:
            self.name = f.name
            try:
                f.write(self.content)
            except:
                os.remove(self.name)
                raise
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        os.remove(self.name)

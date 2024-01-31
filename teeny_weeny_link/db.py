#!/usr/bin/env python
#
# Author:   Daniela Ďuričeková <daniela.duricekova@protonmail.com>
#

"""Access to Redis (our database)."""

import redis


class Database:
    def __init__(self, gen, host='localhost', port=6379, password=None):
        self._gen = gen
        self._conn = redis.Redis(host=host, port=port, password=password)

    def insert_link(self, link):
        id_counter = int(self._conn.incr('id_counter'))
        id = self._gen.to_id(id_counter)
        self._conn.hset(id, 'link', link)
        self._conn.hset(id, 'visit_count', 0)
        return id

    def lookup_link(self, id):
        link = self._conn.hget(id, 'link')
        if link is None:
            return None
        return link.decode()

    def visit_link(self, id):
        link = self.lookup_link(id)
        if link is not None:
            self._conn.hincrby(id, 'visit_count', 1)
        return link

    def get_visit_count(self, id):
        visit_count_str = self._conn.hget(id, 'visit_count')
        if not visit_count_str:
            return None
        return int(visit_count_str)

    def delete_link(self, id):
        self._conn.delete(id)

    def remove_all_links(self):
        self._conn.flushall()

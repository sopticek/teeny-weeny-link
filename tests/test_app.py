#!/usr/bin/env python
#
# Author:   Daniela Ďuričeková <daniela.duricekova@protonmail.com>
#

"""Tests for the app module."""

import json
import unittest

from teeny_weeny_link.app import app
from teeny_weeny_link.app import db


def json_from(response):
    return json.loads(response.data.decode())


class APPTests(unittest.TestCase):
    def setUp(self):
        app.testing = True
        db.remove_all_links()
        self.client = app.test_client()

    def test_insert_link_returns_correct_response(self):
        original_link = 'http://www.google.com'

        response = self.client.post(
            '/links',
            data={'link': original_link}
        )

        self.assertEqual(response.status_code, 200)
        body = json_from(response)
        # id
        self.assertIn('id', body)
        id = body['id']
        # visit_link
        self.assertIn('visit_link', body)
        visit_link = body['visit_link']
        self.assertEqual(
            visit_link,
            'http://localhost/{}'.format(id)
        )
        # visit_count_link
        self.assertIn('visit_count_link', body)
        visit_count_link = body['visit_count_link']
        self.assertEqual(
            visit_count_link,
            'http://localhost/{}/visit_count'.format(id)
        )

    def test_insert_link_adds_http_when_scheme_is_missing(self):
        original_link = 'www.google.com'

        response = self.client.post(
            '/links',
            data={'link': original_link}
        )

        self.assertEqual(response.status_code, 200)
        body = json_from(response)
        visit_link = body['visit_link']
        response = self.client.get(visit_link)
        self.assertEqual(response.status_code, 301)
        self.assertEqual(
            response.headers['Location'],
            'http://' + original_link
        )

    def test_insert_link_returns_error_when_link_is_missing(self):
        response = self.client.post('/links')

        self.assertEqual(response.status_code, 400)
        body = json_from(response)
        self.assertIn('error', body)
        error = body['error']
        self.assertIn('Missing link', error)

    def test_visit_link_redirects_to_original_link(self):
        original_link = 'http://www.google.com'
        response = self.client.post(
            '/links',
            data={'link': original_link}
        )
        body = json_from(response)
        visit_link = body['visit_link']

        response = self.client.get(visit_link)
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response.headers['Location'], original_link)
        body = json_from(response)
        # location
        self.assertIn('location', body)
        location = body['location']
        self.assertEqual(location, original_link)

    def test_visit_link_returns_error_when_id_does_not_exist(self):
        id = 'err'

        response = self.client.get('http://localhost/{}'.format(id))

        self.assertEqual(response.status_code, 404)
        body = json_from(response)
        self.assertIn('error', body)
        error = body['error']
        self.assertIn(id, error)

    def test_get_visit_count_returns_correct_visit_count(self):
        original_link = 'http://www.google.com'
        response = self.client.post(
            '/links',
            data={'link': original_link}
        )
        body = json_from(response)
        visit_link = body['visit_link']
        n = 3
        for i in range(n):
            self.client.get(visit_link)
        visit_count_link = body['visit_count_link']

        response = self.client.get(visit_count_link)

        self.assertEqual(response.status_code, 200)
        body = json_from(response)
        self.assertIn('visit_count', body)
        visit_count = body['visit_count']
        self.assertEqual(visit_count, n)

    def test_get_visit_link_returns_error_when_id_does_not_exist(self):
        id = 'err'

        response = self.client.get(
            'http://localhost/{}/visit_count'.format(id)
        )

        self.assertEqual(response.status_code, 404)
        body = json_from(response)
        self.assertIn('error', body)
        error = body['error']
        self.assertIn(id, error)

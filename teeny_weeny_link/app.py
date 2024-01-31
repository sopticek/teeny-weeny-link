#!/usr/bin/env python
#
# Author:   Daniela Ďuričeková <daniela.duricekova@protonmail.com>
#

"""Main application."""

import flask
import urllib

from teeny_weeny_link.db import Database
from teeny_weeny_link.id_generator import IDGenerator
from teeny_weeny_link.config import parse_our_config_files


app = flask.Flask(__name__)

config = parse_our_config_files()
db = Database(
    gen=IDGenerator(config['id_generator']['salt']),
    host=config['db']['host'],
    port=config['db']['port'],
    password=config['db']['password']
)


@app.route('/links', methods=['POST'])
def insert_link():
    link = flask.request.form.get('link')
    if link is None:
        body = {'error': "Missing link (pass 'link=URL' in POST data)!"}
        return flask.jsonify(body), 400

    link = _validate_link(link)

    id = db.insert_link(link)

    body = {
        'id': id,
        'visit_link': flask.url_for(
            'visit_link',
            id=id,
            _external=True
        ),
        'visit_count_link': flask.url_for(
            'get_visit_count',
            id=id,
            _external=True
        )
    }
    return flask.jsonify(body)


@app.route('/<string:id>')
def visit_link(id):
    link = db.visit_link(id)
    if link is None:
        body = {'error': 'No link for {}!'.format(id)}
        return flask.jsonify(body), 404

    body = {'location': link}
    resp = flask.make_response(flask.jsonify(body))
    resp.headers['Location'] = link
    return resp, 301


@app.route('/<string:id>/visit_count')
def get_visit_count(id):
    visit_count = db.get_visit_count(id)
    if visit_count is None:
        body = {'error': 'No link for {}!'.format(id)}
        return flask.jsonify(body), 404

    body = {'visit_count': visit_count}
    return flask.jsonify(body)


def _validate_link(link):
    # The location header requires the link to have a scheme. Otherwise, if the
    # link was e.g. www.google.com, it would be redirected to
    # http://localhost/www.google.com.
    parsed_link = urllib.parse.urlparse(link)
    if not parsed_link.scheme:
        link = 'http://' + link
    return link

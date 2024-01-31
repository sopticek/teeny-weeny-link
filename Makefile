#
# Project:   teeny-weeny-link
# Copyright: (c) 2017 by Daniela Ďuričeková <daniela.duricekova@protonmail.com>
#            and contributors
# License:   MIT, see the LICENSE file for more details
#

.PHONY: run-dev tests tests-coverage pep8 clean

run-dev:
	@FLASK_APP=teeny_weeny_link/app.py FLASK_DEBUG=1 flask run

tests:
	@# The --output-buffer parameter captures output and prints it after each
	@# failed test (nosetests does this by default).
	@nose2 --output-buffer tests

tests-coverage:
	@nose2 \
		--output-buffer \
		--with-coverage \
		--coverage-report term-missing \
		--coverage-report html \
		--coverage tests \
		--coverage teeny_weeny_link \
		tests

pep8:
	@flake8 teeny_weeny_link/*.py
	@flake8 tests/*

clean:
	@find . -name '__pycache__' -exec rm -rf {} +
	@find . -name '*.py[co]' -exec rm -f {} +
	@rm -rf htmlcov
	@rm -f .coverage

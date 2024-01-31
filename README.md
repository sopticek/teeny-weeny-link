# Teeny Weeny Link #

A simple URL shortener, written in Python, that uses [Redis](https://redis.io/) and [Flask](http://flask.pocoo.org/).

## Requirements ##

The required packages are listed in the `requirements.txt` file. Apart from them, you need to have a Redis server running.

## Installation ##

1. Clone this repository:
```
$ git clone https://github.com/sopticek/teeny-weeny-link
```
2. Enter the `teeny-weeny-link` directory:
```
$ cd teeny-weeny-link
```
3. Create a virtual environment. On Linux, this can be done by the following commands:
```
$ python -m venv virtualenv
$ source virtualenv/bin/activate
```
4. Install all required packages:
```
$ pip install -r requirements.txt
```

## Usage ##

Before using the application, you have to start it in a web server. For example, you may use [gunicorn](http://gunicorn.org/):
```
$ gunicorn teeny_weeny_link.app:app
```

During development, you can also use the built-in Flask web server:
```
$ @FLASK_APP=teeny_weeny_link/app.py FLASK_DEBUG=1 flask run
```

This application provides three different functions. All of them are demonstrated using [curl](https://curl.haxx.se/).

#### Shortening of the Provided URL ####

To shorten a URL (e.g. `www.google.com`), run:
```
$ curl --data 'link=www.google.com' http://127.0.0.1:5000/links
```

In this case, the [POST](https://en.wikipedia.org/wiki/POST_(HTTP)) method is used to send our URL to the application. A [JSON](http://www.json.org/) object of the following structure is returned:
```
{
  "id": "WZ",
  "visit_count_link": "http://127.0.0.1:5000/WZ/visit_count",
  "visit_link": "http://127.0.0.1:5000/WZ"
}
```

The application automatically prefixes the given URL with the `http://` string if the scheme is not provided in the URL. Therefore, if different protocol should be used, you have to include it in the input URL.

#### Accessing the Real URL via the Shortened URL ####

To get the location of the original link, run:
```
$ curl http://127.0.0.1:5000/WZ
```

In this case, the [GET](https://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol#Request_methods) method is used and a [JSON](http://www.json.org/) object of the following structure is returned:
```
{
  "location": "http://www.google.com"
}
```

If you use the shortened URL (`http://127.0.0.1/WZ` in this case) in your browser, you will be automatically redirected to the original link (`www.google.com`).

#### Getting the Visit Count via the Shortened URL ####

To get the visit count for the shortened URL, run:
```
$ curl http://127.0.0.1:5000/WZ/visit_count
```

In this case, we also use the [GET](https://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol#Request_methods) method. A [JSON](http://www.json.org/) object of the following structure is returned:
```
{
  "visit_count": 1
}
```

## Configuration ##

The application uses `.ini` configuration files. The global configuration is stored in `config.ini`. If you want to overwrite some of the configuration, do not edit this file. Instead, create a `config_local.ini` file and specify the changes in there. For testing purposes, create a `config_tests.ini` file and put test-specific configuration there.

When the application is run, it parses all three configuration files. If the same configuration option is present in `config.ini` and `config_local.ini`, the value from the local configuration file (`config_local.ini`) is used. If `config_tests.ini` is present, then it overwrites all configuration options set by `config.ini` and `config_local.ini`.

## Testing ##

The application's code is covered by tests. To execute them, execute `make tests`. It will run the tests by using [nose2](http://nose2.readthedocs.io/en/latest/), so make sure you have it installed.

If you want to generate code coverage, execute `make tests-coverage` and open
`htmlcov/index.html` in your favorite web browser. Once again, you need to
have [nose2](http://nose2.readthedocs.io/en/latest/) installed.

## Notes ##

The application was created in order to get acquainted with [Redis](http://redis-py.readthedocs.io/en/latest/) and [Flask](http://flask.pocoo.org/). Your feedback, suggestions, bug reports, patches, simply anything that can help me to improve this application is welcomed!

## Copyright and License ##

Copyright (c) 2017 Daniela Ďuričeková <daniela.duricekova@protonmail.com> and contributors

Distributed under the MIT license. See the LICENSE file for more details.

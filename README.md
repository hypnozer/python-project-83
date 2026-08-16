# Page Analyzer

[![Actions Status](https://github.com/hypnozer/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/hypnozer/python-project-83/actions)
[![Python CI](https://github.com/hypnozer/python-project-83/actions/workflows/pyci.yml/badge.svg)](https://github.com/hypnozer/python-project-83/actions/workflows/pyci.yml)

Page Analyzer is a Flask web application that checks web pages for SEO
suitability and stores the results in PostgreSQL.

## Demo

<https://python-project-83-ymzv.onrender.com/>

## Features

- URL validation and normalization
- Storage of added websites and check history
- Website availability checks with HTTP status codes
- Extraction of `h1`, `title`, and `description` metadata
- Responsive interface built with Bootstrap

## Built with

- Flask and Jinja2
- PostgreSQL and psycopg
- Requests and Beautiful Soup
- Bootstrap 5
- Gunicorn

## Requirements

- Python 3.12 or newer
- PostgreSQL
- [uv](https://docs.astral.sh/uv/)
- GNU Make

## Setup

Clone the repository and install the dependencies:

```bash
git clone https://github.com/hypnozer/python-project-83.git
cd python-project-83
make install
```

Create a local `.env` file based on `.env.example`. Set the connection URL for
your PostgreSQL database and a random `SECRET_KEY`. Secrets must not be
committed to the repository.

Create the database and apply its schema:

```bash
createdb -U postgres page_analyzer
psql -U postgres -d page_analyzer -f database.sql
```

## Development server

```bash
make dev
```

Open <http://127.0.0.1:5000> in a browser.

## Production server

```bash
make start
```

The server listens on port `8000` by default. Override it with the `PORT`
environment variable when needed.

## Tests and linting

```bash
make check
```

This command runs the test suite and the Ruff linter.

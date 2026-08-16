# Page Analyzer

[![Actions Status](https://github.com/hypnozer/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/hypnozer/python-project-83/actions)
[![Python CI](https://github.com/hypnozer/python-project-83/actions/workflows/pyci.yml/badge.svg)](https://github.com/hypnozer/python-project-83/actions/workflows/pyci.yml)

Page Analyzer is a Flask web application that checks web pages for SEO
suitability and stores the results of the checks.

## Demo

The public Render URL will be added after the first deployment.

## Requirements

- Python 3.12 or newer
- [uv](https://docs.astral.sh/uv/)
- GNU Make

## Setup

```bash
make install
```

Create a local `.env` file based on `.env.example` and set a random
`SECRET_KEY`. Secrets must not be committed to the repository.

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

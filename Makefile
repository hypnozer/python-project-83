install:
	uv sync

update:
	uv lock --upgrade
	uv sync

dev:
	uv run flask --app page_analyzer.app run --debug

start:
	uv run gunicorn -w 5 -b 0.0.0.0:8000 page_analyzer.app:app

test:
	uv run pytest

test-coverage:
	uv run pytest --cov=page_analyzer --cov-report xml

lint:
	uv run ruff check

check: test lint

build:
	uv build

.PHONY: install update dev start test test-coverage lint check build


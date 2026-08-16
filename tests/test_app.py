import importlib
from datetime import date
from unittest.mock import MagicMock

import requests
from flask import Flask, render_template

from page_analyzer import app
from page_analyzer.url_utils import is_valid_url, normalize_url


def test_app_is_exported_from_package():
    assert isinstance(app, Flask)


def test_index():
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert "Анализатор страниц" in response.text
    assert "bootstrap@5.3.8" in response.text
    assert 'action="/urls"' in response.text
    assert 'method="post"' in response.text
    assert 'name="url"' in response.text
    assert 'placeholder="https://www.example.com"' in response.text
    assert "Проверить" in response.text


def test_invalid_url():
    app.config["SECRET_KEY"] = "test-secret"
    client = app.test_client()

    response = client.post("/urls", data={"url": "not a url"})

    assert response.status_code == 422
    assert "Некорректный URL" in response.text
    assert 'value="not a url"' in response.text


def test_url_validation_and_normalization():
    assert is_valid_url("https://example.com/path")
    assert not is_valid_url("example.com")
    assert not is_valid_url("https://" + "a" * 256 + ".com")
    assert normalize_url("HTTPS://Example.COM/path?q=1") == (
        "https://example.com"
    )


def test_url_templates_have_test_attributes():
    url = {
        "id": 1,
        "name": "https://example.com",
        "created_at": date(2026, 8, 16),
        "last_check": date(2026, 8, 17),
        "status_code": None,
    }
    check = {
        "id": 2,
        "status_code": None,
        "h1": None,
        "title": None,
        "description": None,
        "created_at": date(2026, 8, 17),
    }

    with app.test_request_context():
        urls_page = render_template("urls/index.html", urls=[url])
        url_page = render_template("urls/show.html", url=url, checks=[check])

    assert 'data-test="urls"' in urls_page
    assert 'data-test="url"' in url_page
    assert 'data-test="checks"' in url_page
    assert "https://example.com" in urls_page
    assert "2026-08-17" in urls_page
    assert 'action="/urls/1/checks"' in url_page
    assert 'value="Запустить проверку"' in url_page
    assert "2026-08-17" in url_page


def test_create_check(monkeypatch):
    app.config["SECRET_KEY"] = "test-secret"
    app_module = importlib.import_module("page_analyzer.app")
    connection = MagicMock()
    connection.execute.return_value.fetchone.return_value = {
        "id": 1,
        "name": "https://example.com",
    }
    connection_context = MagicMock()
    connection_context.__enter__.return_value = connection
    monkeypatch.setattr(app_module, "connect", lambda: connection_context)
    response_from_site = MagicMock(status_code=200)
    get = MagicMock(return_value=response_from_site)
    monkeypatch.setattr(app_module.requests, "get", get)

    client = app.test_client()
    response = client.post("/urls/1/checks")

    assert response.status_code == 302
    assert response.location.endswith("/urls/1")
    get.assert_called_once_with("https://example.com", timeout=10)
    response_from_site.raise_for_status.assert_called_once_with()
    insert_params = connection.execute.call_args_list[1].args[1]
    assert insert_params[:2] == (1, 200)
    with client.session_transaction() as session:
        assert (
            "success",
            "Страница успешно проверена",
        ) in session["_flashes"]


def test_request_error_does_not_create_check(monkeypatch):
    app.config["SECRET_KEY"] = "test-secret"
    app_module = importlib.import_module("page_analyzer.app")
    connection = MagicMock()
    connection.execute.return_value.fetchone.return_value = {
        "id": 1,
        "name": "https://example.com",
    }
    connection_context = MagicMock()
    connection_context.__enter__.return_value = connection
    monkeypatch.setattr(app_module, "connect", lambda: connection_context)
    monkeypatch.setattr(
        app_module.requests,
        "get",
        MagicMock(side_effect=requests.RequestException),
    )

    client = app.test_client()
    response = client.post("/urls/1/checks")

    assert response.status_code == 302
    assert connection.execute.call_count == 1
    with client.session_transaction() as session:
        assert (
            "danger",
            "Произошла ошибка при проверке",
        ) in session["_flashes"]

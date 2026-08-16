from flask import Flask

from page_analyzer import app


def test_app_is_exported_from_package():
    assert isinstance(app, Flask)


def test_index():
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert "Анализатор страниц" in response.text

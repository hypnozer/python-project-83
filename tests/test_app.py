from flask import Flask

from page_analyzer import app


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

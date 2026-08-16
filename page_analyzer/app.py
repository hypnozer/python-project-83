import os
from datetime import date

import psycopg
from dotenv import load_dotenv
from flask import (
    Flask,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from page_analyzer.database import connect
from page_analyzer.url_utils import is_valid_url, normalize_url

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/urls")
def urls_index():
    with connect() as connection:
        urls = connection.execute(
            """
            SELECT
                urls.id,
                urls.name,
                urls.created_at,
                latest_check.created_at AS last_check,
                latest_check.status_code
            FROM urls
            LEFT JOIN LATERAL (
                SELECT created_at, status_code
                FROM url_checks
                WHERE url_id = urls.id
                ORDER BY id DESC
                LIMIT 1
            ) AS latest_check ON TRUE
            ORDER BY urls.id DESC
            """
        ).fetchall()

    return render_template("urls/index.html", urls=urls)


@app.post("/urls")
def urls_create():
    raw_url = request.form.get("url", "").strip()
    if not is_valid_url(raw_url):
        flash("Некорректный URL", "danger")
        return render_template("index.html", url=raw_url), 422

    normalized_url = normalize_url(raw_url)

    with connect() as connection:
        new_url = connection.execute(
            """
            INSERT INTO urls (name, created_at)
            VALUES (%s, %s)
            ON CONFLICT (name) DO NOTHING
            RETURNING id
            """,
            (normalized_url, date.today()),
        ).fetchone()

        if new_url:
            url_id = new_url["id"]
            flash("Страница успешно добавлена", "success")
        else:
            existing_url = connection.execute(
                "SELECT id FROM urls WHERE name = %s",
                (normalized_url,),
            ).fetchone()
            url_id = existing_url["id"]
            flash("Страница уже существует", "info")

    return redirect(url_for("url_show", url_id=url_id))


@app.get("/urls/<int:url_id>")
def url_show(url_id):
    with connect() as connection:
        url = connection.execute(
            """
            SELECT id, name, created_at
            FROM urls
            WHERE id = %s
            """,
            (url_id,),
        ).fetchone()

        if url is None:
            abort(404)

        checks = connection.execute(
            """
            SELECT id, status_code, h1, title, description, created_at
            FROM url_checks
            WHERE url_id = %s
            ORDER BY id DESC
            """,
            (url_id,),
        ).fetchall()

    return render_template("urls/show.html", url=url, checks=checks)


@app.post("/urls/<int:url_id>/checks")
def checks_create(url_id):
    try:
        with connect() as connection:
            check = connection.execute(
                """
                INSERT INTO url_checks (url_id, created_at)
                SELECT id, %s
                FROM urls
                WHERE id = %s
                RETURNING id
                """,
                (date.today(), url_id),
            ).fetchone()

            if check is None:
                abort(404)
    except psycopg.Error:
        flash("Произошла ошибка при проверке", "danger")
    else:
        flash("Страница успешно проверена", "success")

    return redirect(url_for("url_show", url_id=url_id))


def main():
    app.run()


if __name__ == "__main__":
    main()

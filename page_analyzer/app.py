import os
from datetime import date

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
            SELECT id, name, created_at
            FROM urls
            ORDER BY id DESC
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

    return render_template("urls/show.html", url=url)


def main():
    app.run()


if __name__ == "__main__":
    main()

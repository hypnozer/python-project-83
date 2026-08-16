from bs4 import BeautifulSoup


def extract_seo_data(html):
    soup = BeautifulSoup(html, "html.parser")
    description_tag = soup.find("meta", attrs={"name": "description"})

    return {
        "h1": _get_tag_text(soup.find("h1")),
        "title": _get_tag_text(soup.find("title")),
        "description": _get_description(description_tag),
    }


def _get_tag_text(tag):
    if tag is None:
        return ""
    return tag.get_text(" ", strip=True)


def _get_description(tag):
    if tag is None:
        return ""
    return tag.get("content", "").strip()

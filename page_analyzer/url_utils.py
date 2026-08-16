from urllib.parse import urlparse

import validators

MAX_URL_LENGTH = 255


def is_valid_url(url):
    return len(url) <= MAX_URL_LENGTH and validators.url(url) is True


def normalize_url(url):
    parsed_url = urlparse(url)
    scheme = parsed_url.scheme.lower()
    netloc = parsed_url.netloc.lower()
    return f"{scheme}://{netloc}"


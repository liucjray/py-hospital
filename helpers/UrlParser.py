import urllib.parse as urlparse


def get_qs(url: str, key: str, default=None):
    try:
        parsed = urlparse.urlparse(url)
        return urlparse.parse_qs(parsed.query)[key][0]
    except KeyError:
        return default

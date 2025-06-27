from urllib.parse import urlparse
import validators


def validate_url(url):
    """Validate URL format"""
    if not url:
        return False, "URL is required"

    if not validators.url(url):
        return False, "Invalid URL format"

    # Ensure URL has scheme (http or https)
    parsed = urlparse(url)
    if not parsed.scheme:
        url = f"http://{url}"

    return True, url
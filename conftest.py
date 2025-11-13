import os
import pytest
import requests
from dotenv import load_dotenv
from urllib3.exceptions import InsecureRequestWarning
import urllib3

# Automatically load environment variables from .env
load_dotenv()

# Disable self-signed certificate warnings globally
urllib3.disable_warnings(InsecureRequestWarning)


@pytest.fixture(scope="session")
def base_url() -> str:
    url = os.getenv("UOS_API_URL")
    if not url:
        raise RuntimeError("Missing UOS_API_URL in .env")
    return url.rstrip("/")


@pytest.fixture(scope="session")
def api_key() -> str:
    key = os.getenv("UOS_API_KEY")
    if not key:
        raise RuntimeError("Missing UOS_API_KEY in .env")
    return key


@pytest.fixture(scope="session")
def session(api_key: str):
    """
    Reusable HTTP session with authorization header.
    All requests will ignore SSL verification (self-signed certs).
    """
    s = requests.Session()
    s.headers.update({
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-API-KEY": api_key
    })

    # Add default verify=False to all requests
    original_request = s.request

    def request_with_verify(method, url, **kwargs):
        if "verify" not in kwargs:
            kwargs["verify"] = False
        return original_request(method, url, **kwargs)

    s.request = request_with_verify

    yield s
    s.close()


@pytest.fixture(scope="session")
def site_id(session, base_url):
    """
    Retrieve the first available site if UOS_SITE_ID not set.
    """
    env_site = os.getenv("UOS_SITE_ID")
    if env_site:
        return env_site

    response = session.get(f"{base_url}/v1/sites")
    response.raise_for_status()
    data = response.json()
    if not data.get("data"):
        raise RuntimeError("No sites found on the server.")
    return data["data"][0].get("id") or data["data"][0].get("_id")
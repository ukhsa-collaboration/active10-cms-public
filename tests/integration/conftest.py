import os
from collections.abc import Generator

import httpx
import pytest

from .utils import is_url


@pytest.fixture(scope="session")
def base_url() -> str:
    url = os.getenv("API_BASE_URL") or os.getenv("BASE_URL")
    if not url or not is_url(url):
        pytest.fail("Set API_BASE_URL (or BASE_URL) to the HTTP(S) URL of a running CMS.", pytrace=False)
    return url.rstrip("/")


@pytest.fixture
def client(base_url) -> Generator[httpx.Client, None, None]:
    headers = {"User-Agent": "Integration Tests UA/1.0"}
    with httpx.Client(base_url=base_url, follow_redirects=False, headers=headers, timeout=5.0) as connection:
        yield connection


@pytest.fixture
def admin_credentials():
    username = os.getenv("ACTIVE10_ADMIN_USERNAME")
    password = os.getenv("ACTIVE10_ADMIN_PASSWORD")
    if not username or not password:
        pytest.skip("Set ACTIVE10_ADMIN_USERNAME and ACTIVE10_ADMIN_PASSWORD to run authenticated admin tests.")
    return username, password


def pytest_addoption(parser):
    parser.addoption(
        "--require-content",
        action="store_true",
        default=False,
        help="Fail instead of skipping content-dependent checks when CMS collections are empty.",
    )


@pytest.fixture
def require_content(request):
    def check(records, description):
        assert isinstance(records, list), f"{description}: expected a JSON list"
        if not records:
            message = f"{description}: no content available"
            if request.config.getoption("--require-content"):
                pytest.fail(message)
            pytest.skip(message)
        return records

    return check


@pytest.fixture
def admin_write_environment(base_url):
    from urllib.parse import urlparse

    environment = os.getenv("DEPLOY_ENVIRONMENT", "").lower()
    hostname = urlparse(base_url).hostname or ""
    if environment in {"prd", "prod", "production"} or hostname in {
        "active10.prod.phedigital.co.uk",
        "cms.phedigital.co.uk",
    }:
        pytest.fail("Admin write tests cannot run against production.", pytrace=False)
    if os.getenv("ACTIVE10_ALLOW_ADMIN_WRITES") != "true":
        pytest.fail("Set ACTIVE10_ALLOW_ADMIN_WRITES=true for a dedicated test environment.", pytrace=False)

import re
from html import unescape
from urllib.parse import parse_qs, urlparse
from uuid import uuid4

import pytest

from .admin_helpers import ADMIN_PAGE_ENDPOINT, extract_csrf_token, login_to_admin
from .utils import assert_status, get_json

FAQ_ADD_ENDPOINT = "/dhsc-admin/faq/faq/add/"
FAQ_API_ENDPOINT = "/api/v1/active10/faq/"
FAQ_LIST_ENDPOINT = "/dhsc-admin/faq/faq/"


def test_admin_login_with_invalid_credentials(client, base_url):
    form_url = f"{base_url}{ADMIN_PAGE_ENDPOINT}"
    response = client.get(form_url)
    assert_status(response, 200, include_body=False)
    token = extract_csrf_token(response.text)
    response = client.post(
        form_url,
        data={
            "csrfmiddlewaretoken": token,
            "login_view-current_step": "auth",
            "auth-username": f"nonexistent-{uuid4()}",
            "auth-password": "incorrect-password",  # pragma: allowlist secret
        },
        headers={"Referer": form_url},
    )
    assert_status(response, 200, include_body=False)
    assert "Please enter a correct username and password" in response.text
    admin_page = client.get("/dhsc-admin/")
    assert_status(admin_page, 302, include_body=False)
    redirect = urlparse(admin_page.headers["location"])
    assert redirect.path == "/dhsc-admin/login/"
    assert parse_qs(redirect.query).get("next") == ["/dhsc-admin/"]


@pytest.mark.authenticated
def test_admin_login_with_valid_credentials(client, base_url, admin_credentials):
    login_to_admin(client, base_url, *admin_credentials)
    admin_page = client.get("/dhsc-admin/")
    assert_status(admin_page, 200, include_body=False)
    assert "site administration" in admin_page.text.lower()


def _find_faq_id(client, title):
    # Admin lookup remains usable even when the public FAQ endpoint fails.
    response = client.get(FAQ_LIST_ENDPOINT, params={"q": title})
    assert_status(response, 200, include_body=False)
    matches = re.findall(r"href=[\'\"]([^\'\"]*/(\d+)/change/)[\'\"][^>]*>(.*?)</a>", response.text, re.DOTALL)
    ids = [entry_id for _, entry_id, label in matches if unescape(re.sub(r"<[^>]+>", "", label)) == title]
    assert len(ids) <= 1, "Test FAQ title is not unique"
    return ids[0] if ids else None


def _delete_faq(client, entry_id, base_url):
    url = f"{base_url}{FAQ_LIST_ENDPOINT}{entry_id}/delete/"
    response = client.get(url)
    assert_status(response, 200, include_body=False)
    token = extract_csrf_token(response.text)
    response = client.post(url, data={"csrfmiddlewaretoken": token, "post": "yes"}, headers={"Referer": url})
    assert_status(response, 302, include_body=False)
    assert urlparse(response.headers["location"]).path == FAQ_LIST_ENDPOINT


@pytest.mark.admin_write
@pytest.mark.authenticated
def test_admin_can_create_and_delete_faq_entry(client, base_url, admin_credentials, admin_write_environment, request):
    title = f"Integration test FAQ {uuid4()}"
    text = "Integration test content"
    login_to_admin(client, base_url, *admin_credentials)
    entry_id = None
    created = False

    def cleanup():
        cleanup_id = entry_id or _find_faq_id(client, title)
        if cleanup_id:
            _delete_faq(client, cleanup_id, base_url)
            assert _find_faq_id(client, title) is None, "Test FAQ still present after cleanup"
        elif created:
            pytest.fail("Created FAQ could not be located for cleanup")

    add_url = f"{base_url}{FAQ_ADD_ENDPOINT}"
    page = client.get(add_url)
    assert_status(page, 200, include_body=False)
    token = extract_csrf_token(page.text)
    # Register cleanup before attempting a write, including transport/API failures.
    request.addfinalizer(cleanup)
    response = client.post(
        add_url,
        data={
            "csrfmiddlewaretoken": token,
            "title": title,
            "text": text,
            "list_order": "0",
            "activity_type": "walking",
            "_continue": "Save and continue editing",
        },
        headers={"Referer": add_url},
    )
    assert_status(response, 302, include_body=False)
    created = True
    location = urlparse(response.headers["location"]).path
    match = re.fullmatch(r"/dhsc-admin/faq/faq/(\d+)/change/", location)
    assert match, f"Unexpected FAQ save redirect: {location}"
    entry_id = match.group(1)
    faqs = get_json(client, FAQ_API_ENDPOINT)
    entries = [entry for entry in faqs if entry["id"] == int(entry_id)]
    assert len(entries) == 1, "Created FAQ missing from public API"
    assert entries[0]["title"] == title
    assert entries[0]["text"] == text

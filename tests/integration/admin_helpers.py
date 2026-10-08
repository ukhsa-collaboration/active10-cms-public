import re
from urllib.parse import urlparse

from .utils import assert_status

ADMIN_PAGE_ENDPOINT = "/account/login/"


def extract_csrf_token(html: str) -> str:
    match = re.search(
        r"name=['\"]csrfmiddlewaretoken['\"][^>]*value=['\"]([^'\"]+)",
        html,
        flags=re.IGNORECASE,
    )
    assert match, "csrfmiddlewaretoken input not found in HTML"
    return match.group(1)


def login_to_admin(client, base_url: str, username: str, password: str):
    form_url = f"{base_url}{ADMIN_PAGE_ENDPOINT}"

    response = client.get(form_url)
    assert_status(response, 200, include_body=False)
    token = extract_csrf_token(response.text)

    data = {
        "csrfmiddlewaretoken": token,
        "login_view-current_step": "auth",
        "auth-username": username,
        "auth-password": password,
    }
    headers = {"Referer": form_url}

    login_response = client.post(form_url, data=data, headers=headers)
    assert_status(login_response, 302, include_body=False)
    assert urlparse(login_response.headers["location"]).path == "/account/two_factor/", (
        "Login did not complete; check credentials and OTP requirements"
    )
    return login_response

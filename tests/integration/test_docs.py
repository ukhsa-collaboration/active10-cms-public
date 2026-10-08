import pytest

from .admin_helpers import login_to_admin
from .utils import assert_status

DOCS_ENDPOINT = "/ap/docs/"
pytestmark = pytest.mark.debug_docs


def test_unauthenticated_docs_not_allowed(client):
    response = client.get(DOCS_ENDPOINT)
    assert_status(response, 403)


@pytest.mark.authenticated
def test_docs_available_after_login(client, base_url, admin_credentials):
    username, password = admin_credentials
    login_to_admin(client, base_url, username, password)
    response = client.get(DOCS_ENDPOINT)
    assert_status(response, 200)
    assert "swagger" in response.text.lower(), "Swagger UI markup missing from docs response"

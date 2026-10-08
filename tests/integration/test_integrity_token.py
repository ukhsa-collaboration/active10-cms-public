import pytest

from .utils import assert_status

NEW_INTEGRITY_URL_PATH = "/api/v1/new-check-integrity-token"
LEGACY_INTEGRITY_URL_PATH = "/api/v1/check-integrity-token"
params = {"format": "json"}


@pytest.mark.parametrize("path", [NEW_INTEGRITY_URL_PATH, LEGACY_INTEGRITY_URL_PATH])
def test_integrity_get_not_allowed(client, base_url, path):
    resp = client.get(f"{base_url}{path}", params=params)
    assert_status(resp, 405)


@pytest.mark.external
def test_integrity_new_invalid_token_returns_decode_error(client, base_url):
    url = f"{base_url}{NEW_INTEGRITY_URL_PATH}"
    resp = client.post(url, json={"integrityToken": "dummy"}, params=params)
    assert_status(resp, 500)
    body = resp.json()
    assert "Failed to decode integrity token" in body.get("error", "")


@pytest.mark.parametrize(
    "payload",
    [None, {}],
)
@pytest.mark.external
def test_integrity_new_missing_token_returns_400(client, base_url, payload):
    url = f"{base_url}{NEW_INTEGRITY_URL_PATH}"
    json_payload = payload if payload is not None else None
    resp = client.post(url, json=json_payload, params=params)
    assert_status(resp, 400)
    body = resp.json()
    assert body.get("error") == "Missing integrityToken"


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"integrityToken": "dummy"},
    ],
)
@pytest.mark.external
def test_integrity_legacy_returns_google_error_structure(client, base_url, payload):
    url = f"{base_url}{LEGACY_INTEGRITY_URL_PATH}"
    resp = client.post(url, json=payload, params=params)
    assert_status(resp, 400)
    body = resp.json()
    assert isinstance(body.get("error"), dict), "Legacy endpoint should proxy Google error payload"
    assert body["error"].get("status") == "INVALID_ARGUMENT"
    assert "Integrity token" in body["error"].get("message", "")

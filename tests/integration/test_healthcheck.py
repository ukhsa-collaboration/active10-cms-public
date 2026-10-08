from .utils import assert_status

HEALTHCHECK_ENDPOINT = "/healthcheck"
params = {"format": "json"}


def test_healthcheck(client, base_url):
    r = client.get(f"{base_url}{HEALTHCHECK_ENDPOINT}", params=params)
    assert_status(r, 200)
    data = r.json()

    assert isinstance(data, dict)
    assert "DatabaseBackend" in data and "MigrationsHealthCheck" in data

    assert data["DatabaseBackend"] == "working"
    assert data["MigrationsHealthCheck"] == "working"

from urllib.parse import urlparse


def is_url(value: str) -> bool:
    """Return True when *value* looks like a HTTP(S) URL."""
    try:
        parsed = urlparse(value)
        return parsed.scheme in {"http", "https"} and bool(parsed.netloc)
    except ValueError:
        return False


def assert_status(response, expected: int, *, include_body: bool = True) -> None:
    excerpt = response.text[:500] if include_body else "(body omitted)"
    assert response.status_code == expected, (
        f"{response.request.method} {response.request.url}: expected {expected}, "
        f"got {response.status_code}; response: {excerpt}"
    )


def get_json(client, path: str, params=None):
    response = client.get(path, params={"format": "json", **(params or {})})
    assert_status(response, 200)
    assert "application/json" in response.headers.get("content-type", ""), f"{path}: expected JSON content type"
    return response.json()


def assert_fields(record, fields) -> None:
    assert isinstance(record, dict), f"Expected an object, got {record!r}"
    for name, field_type in fields.items():
        assert name in record, f"Missing {name!r} in {record!r}"
        assert type(record[name]) is field_type, f"{name}: expected {field_type.__name__}, got {record[name]!r}"

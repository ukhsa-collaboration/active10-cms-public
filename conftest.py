"""Project-wide pytest configuration."""

import os

from django.conf import settings


def pytest_configure(config):
    # settings.SECRET_KEY comes from DJANGO_SECRET_KEY and defaults to "", which makes any request
    # (sessions, CSRF, signing) fail. Tests get a throwaway key unless one is provided explicitly.
    if not os.environ.get("DJANGO_SECRET_KEY"):
        settings.SECRET_KEY = "insecure-test-only-secret-key"  # noqa: S105  # pragma: allowlist secret

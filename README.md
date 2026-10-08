## Pre-commit hooks

This repo uses pre-commit to run common quality and security checks before each commit to prevent easy-to-catch issues from reaching the workflow.

## Installing

```bash
python -m pip install --upgrade pre-commit ruff detect-secrets
pre-commit install
```

Once installed, all of the checks in `.pre-commit-config.yaml` must pass before you can commit any files to the repo.

## How to run project with Docker

1. Install [Docker](https://docs.docker.com/install/) and [Docker Compose](https://docs.docker.com/compose/install/)
2. Run commands:
    - `docker-compose build`
    - `docker volume create --name=active10_db`
    - `docker-compose up`
    - `docker-compose exec api python manage.py migrate`
    - `docker-compose exec api python manage.py loaddata fixtures.json`
3. Create admin user:
    - `docker-compose exec api python manage.py createsuperuser`
4. Run tests
    - `docker-compose run api python manage.py test applications`
5. [Login](http://127.0.0.1:8000/dhsc-admin/) as Admin and check the [Docs](http://127.0.0.1:8000/ap/docs/)

## Integration tests

Install the lightweight HTTP test dependencies and run the deployment checks
against a running CMS:

```bash
python -m pip install -r tests/integration/requirements.txt
API_BASE_URL=http://127.0.0.1:8000 python -m pytest -c pyproject.toml tests/integration
```

| Selection | Requirements |
| --- | --- |
| `-m external` | External content sites and configured Google credentials/services |
| `-m 'authenticated and not admin_write and not debug_docs'` | Admin credentials and a login that completes without an OTP challenge |
| `-m admin_write` | Credentials, a dedicated test environment and `ACTIVE10_ALLOW_ADMIN_WRITES=true` |
| `-m debug_docs` | Development CMS exposing `/ap/docs/`; credentials for the authenticated check |

Set `ACTIVE10_ADMIN_USERNAME` and `ACTIVE10_ADMIN_PASSWORD` for authenticated
checks. They skip locally when credentials are absent. Secure session/CSRF cookies
require HTTPS for admin tests. Non-development environments enforce 2FA, so
password-only login may not be sufficient.

The deployment pipeline allows empty content in dev and requires content in uat
and prd. Content-dependent tests skip if a collection or singleton is empty. Use `--require-content`
in a populated test environment to make that a failure. Rewards list, missing
slug/category and rejected-write checks run even when rewards are empty; detail
and category checks are independent for each version.

Google POST checks are optional because even missing-token validation requires
service-account configuration in the current implementation. The new endpoint
returns 500 for an invalid token after Google rejects it; the legacy endpoint
proxies Google's error response. Neither test obtains a genuine device token.

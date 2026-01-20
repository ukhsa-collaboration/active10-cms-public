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
5. [Login](http://127.0.0.1:8000/admin/) as Admin and check the [Docs](http://127.0.0.1:8000/api/v1/active10/docs/)

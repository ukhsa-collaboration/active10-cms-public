from os import getenv

import boto3


def _env_truthy(value):
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


def generate_rds_iam_token(host, port, user):
    session = boto3.Session()
    client = session.client("rds")
    return client.generate_db_auth_token(
        DBHostname=host,
        Port=int(port),
        DBUsername=user,
    )


def db_password():
    if not _env_truthy(getenv("DB_IAM_AUTH", "")):
        return getenv("DB_PASSWORD", "")

    host = getenv("DB_HOST", "localhost")
    port = getenv("DB_PORT", "5432")
    user = getenv("DB_USER", "postgres")

    return generate_rds_iam_token(host, port, user)

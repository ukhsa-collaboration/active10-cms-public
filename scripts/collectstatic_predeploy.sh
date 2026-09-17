#!/usr/bin/env bash
# Runs collectstatic once before deploy so new static assets exist in S3 before the ECS task definition is updated.
# Expects DEPLOY_ENVIRONMENT to be set by the calling deploy workflow (e.g. dev, uat, prd).
set -euo pipefail

: "${DEPLOY_ENVIRONMENT:?DEPLOY_ENVIRONMENT must be set}"

export AWS_STORAGE_BUCKET_NAME="aw-active10-euw2-${DEPLOY_ENVIRONMENT}-s3-media"
export DJANGO_SETTINGS_MODULE=active10.settings

python3 -m venv .venv-collectstatic
# shellcheck disable=SC1091
source .venv-collectstatic/bin/activate

pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt

python manage.py collectstatic --noinput

deactivate
rm -rf .venv-collectstatic

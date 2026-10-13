#!/usr/bin/env bash
# Collect from the release image before updating the ECS service.
# DEPLOY_ENVIRONMENT and DEPLOY_IMAGE are supplied by the deploy workflow.
set -euo pipefail

: "${DEPLOY_ENVIRONMENT:?DEPLOY_ENVIRONMENT must be set}"
: "${DEPLOY_IMAGE:?DEPLOY_IMAGE must be set}"
: "${AWS_REGION:?AWS_REGION must be set}"

export AWS_STORAGE_BUCKET_NAME="aw-active10-euw2-${DEPLOY_ENVIRONMENT}-s3-media"

# Authenticate to the release image's ECR registry using the deploy role.
registry_hostname="${DEPLOY_IMAGE%%/*}"
docker_config_dir=$(mktemp -d)
trap 'rm -rf "$docker_config_dir"' EXIT
export DOCKER_CONFIG="$docker_config_dir"

echo "$(date -u +%FT%TZ) Authenticating to release image registry"
aws ecr get-login-password --region "$AWS_REGION" |
  docker login --username AWS --password-stdin "$registry_hostname"

echo "$(date -u +%FT%TZ) Pulling release image: $DEPLOY_IMAGE"
docker pull "$DEPLOY_IMAGE"

echo "$(date -u +%FT%TZ) Starting collectstatic from release image"
docker run --rm \
  --entrypoint python \
  --env AWS_ACCESS_KEY_ID \
  --env AWS_SECRET_ACCESS_KEY \
  --env AWS_SESSION_TOKEN \
  --env AWS_REGION \
  --env AWS_DEFAULT_REGION \
  --env AWS_STORAGE_BUCKET_NAME \
  --env DJANGO_SETTINGS_MODULE=active10.settings \
  "$DEPLOY_IMAGE" \
  -u manage.py collectstatic --noinput --verbosity 2

echo "$(date -u +%FT%TZ) Static asset predeploy finished"

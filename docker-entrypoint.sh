#!/usr/bin/env bash
set -euo pipefail

: "${GUNICORN_PORT:=80}"
: "${GUNICORN_WORKERS:=1}"
: "${GUNICORN_TIMEOUT:=30}"
: "${GUNICORN_WSGI_MODULE:=active10.wsgi:application}"
: "${DJANGO_MIGRATE:=1}"
: "${DJANGO_COLLECTSTATIC:=1}"
: "${DJANGO_DEV_SERVER:=0}"
: "${USE_MEMCACHED:=1}"


# Start memcached service
if [[ "${USE_MEMCACHED}" == "1" ]]; then
    echo "Start memcached service"
    service memcached start
fi

if [[ "${DJANGO_DEV_SERVER}" != "1" ]]; then
  echo "Running Django deploy checks"
  python manage.py check --deploy
fi

if [[ "${DJANGO_MIGRATE}" == "1" ]]; then
  echo "Applying database migrations"
  python manage.py migrate --noinput
else
  echo "Skipping migrations (MIGRATE=${DJANGO_MIGRATE})"
fi

if [[ "${DJANGO_COLLECTSTATIC}" == "1" ]]; then
  echo "Collecting static files"
  python manage.py collectstatic --noinput
else
  echo "Skipping collectstatic (COLLECTSTATIC=${DJANGO_COLLECTSTATIC})"
fi

echo "Starting application"
if [[ "${DJANGO_DEV_SERVER}" == "1" ]]; then
  echo "DEV_SERVER=1 -> using runserver on 0.0.0.0:${GUNICORN_PORT}"
  exec python manage.py runserver 0.0.0.0:"${GUNICORN_PORT}"
else
  echo "Using Gunicorn (${GUNICORN_WORKERS} workers) on 0.0.0.0:${GUNICORN_PORT}"
  exec gunicorn "${GUNICORN_WSGI_MODULE}" \
      --bind 0.0.0.0:"${GUNICORN_PORT}" \
      --workers "${GUNICORN_WORKERS}" \
      --timeout "${GUNICORN_TIMEOUT}" \
      --graceful-timeout 30 \
      --access-logfile '-' --error-logfile '-'
fi

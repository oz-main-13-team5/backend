#!/usr/bin/env bash
set -euo pipefail

# Ensure we run from the project root (where manage.py lives)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# (Optional) Wait for DB if host/port provided
if command -v pg_isready >/dev/null 2>&1; then
  DB_HOST_NAME="${DB_HOST:-localhost}"
  DB_PORT_NUM="${DB_PORT:-5432}"
  echo "⏳ Waiting for Postgres at ${DB_HOST_NAME}:${DB_PORT_NUM} ..."
  for i in $(seq 1 30); do
    if pg_isready -h "${DB_HOST_NAME}" -p "${DB_PORT_NUM}" >/dev/null 2>&1; then
      echo "✅ Postgres is ready."
      break
    fi
    sleep 1
    if [ "$i" -eq 30 ]; then
      echo "❌ Postgres not ready after 30s"; exit 1
    fi
  done
fi

echo "📦 Running migrations..."
uv run python manage.py migrate --noinput

echo "🗂  Collecting static files..."
uv run python manage.py collectstatic --noinput

echo "🚀 Starting Gunicorn..."
uv run gunicorn config.wsgi:application \
  --chdir "${PROJECT_ROOT}" \
  --bind 0.0.0.0:8000 \
  --workers "${GUNICORN_WORKERS:-3}" \
  --timeout "${GUNICORN_TIMEOUT:-60}"

#!/usr/bin/env sh
set -e

echo "⏳ Waiting for MySQL at $DB_HOST:$DB_PORT..."
until nc -z "$DB_HOST" "$DB_PORT"; do
  sleep 1
done
echo "✅ MySQL is up."

/venv/bin/python -m pip show django || true
/venv/bin/python manage.py migrate --noinput
exec /venv/bin/python manage.py runserver 0.0.0.0:8000
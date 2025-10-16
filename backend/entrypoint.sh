#!/usr/bin/env sh
set -e

echo "⏳ Waiting for MySQL at $DB_HOST:$DB_PORT..."
until nc -z "$DB_HOST" "$DB_PORT"; do
  sleep 1
done
echo "✅ MySQL is up."

python manage.py migrate --noinput
python manage.py runserver 0.0.0.0:8000
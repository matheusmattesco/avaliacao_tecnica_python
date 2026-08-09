#!/bin/sh

echo "Waiting for database..."

while ! python -c "
import os, psycopg, sys
try:
    psycopg.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
    )
    sys.exit(0)
except Exception:
    sys.exit(1)
"; do
    sleep 1
done

echo "Database is ready."

if [ "${RUN_MIGRATIONS:-true}" = "true" ]; then
    echo "Running migrations..."
    python manage.py migrate --noinput
fi

exec "$@"

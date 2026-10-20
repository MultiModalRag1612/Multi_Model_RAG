#!/bin/sh
set -e

echo "Running database migration"

cd /app/models/db_schemes/alembic/
alembic -c alembic.ini upgrade head

cd /app
exec "$@"
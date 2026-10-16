set -e
echo "Running database mugration"
cd /app/models/db_schemes/alembic/
alembic upgrade head 
cd /app
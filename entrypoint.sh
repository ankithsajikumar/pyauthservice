#!/bin/bash
# Docker entrypoint script for PyAuthService
# Handles migrations and container startup

set -e

echo "🐳 PyAuthService - Starting..."

# Wait for database to be ready only when using a network database
if [ -n "${DB_HOST:-}" ] && [ "${DB_HOST}" != "sqlite" ]; then
  echo "⏳ Waiting for database at ${DB_HOST}:${DB_PORT:-5432}..."
  while ! nc -z "${DB_HOST}" "${DB_PORT:-5432}"; do
    sleep 1
  done
  echo "✅ Database is ready"
else
  echo "📁 Using local SQLite database; skipping external DB wait."
fi

# Run migrations
echo "🔄 Running database migrations..."
python manage.py migrate --noinput

# Collect static files (if needed)
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput || true

# Create superuser if it doesn't exist (optional, for development)
if [ "$DEBUG" = "True" ]; then
  python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    print("✅ Superuser 'admin' created (use in development only!)")
else:
    print("✅ Superuser already exists")
END
fi

echo "🚀 Starting PyAuthService..."

# Execute the main command
exec "$@"

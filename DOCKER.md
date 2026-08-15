# Docker Setup Guide for PyAuthService

This guide covers Docker deployment, development, and troubleshooting for PyAuthService.

## Quick Start

```bash
# 1. Copy environment template
cp .env.example .env

# 2. Start all services
docker-compose up -d

# 3. Check if everything is running
docker-compose ps

# 4. View logs
docker-compose logs -f app

# 5. Access application
# App: http://localhost:8000
# Admin: http://localhost:8000/admin (user: admin, pass: admin)
```

## File Structure

```
pyauthservice/
├── Dockerfile              # Official production Dockerfile
├── docker-compose.yml      # Production-ready compose file
├── docker-compose.override.yml  # Development overrides (not git-tracked)
├── .dockerignore           # Files to exclude from Docker build
├── entrypoint.sh           # Container startup script (runs migrations)
├── docker-validate.sh      # Script to validate Docker setup
├── Makefile               # Convenient Docker commands
├── .env.example           # Environment template
└── .env                   # Your secrets (never commit!)
```

## Services

### 1. App Service
**Image**: `pyauthservice:latest` (built locally)  
**Port**: 8000  
**Database**: PostgreSQL via environment variable `DATABASE_URL`

The entrypoint script automatically:
- Waits for database to be ready
- Runs `python manage.py migrate`
- Collects static files
- Creates default superuser (dev only)

### 2. Database Service
**Image**: `postgres:15-alpine`  
**Port**: 5432  
**Credentials**: 
- User: `authuser`
- Password: `authpassword`
- Database: `pyauthservice`

**Volume**: `postgres-data` (persists between restarts)

### 3. Cache Service (Redis)
**Image**: `redis:7-alpine`  
**Port**: 6379  
**Purpose**: Session/token caching (optional, can be disabled)

## Development Workflow

### Run Development Server with Hot Reload

The `docker-compose.override.yml` automatically loads and applies:
- Django development server instead of gunicorn
- `/app` volume mount for instant code reloading
- Debug mode enabled

```bash
# Start with auto-reload
docker-compose up -d

# Edit your code, changes appear instantly!
# View logs:
docker-compose logs -f app
```

### Common Development Tasks

```bash
# Run migrations
docker-compose exec app python manage.py migrate

# Create database
docker-compose exec app python manage.py migrate --run-syncdb

# Create superuser
docker-compose exec app python manage.py createsuperuser

# Run tests
docker-compose exec app python manage.py test

# Django shell
docker-compose exec app python manage.py shell

# Jump into container
docker-compose exec app bash

# View logs
docker-compose logs -f app

# Stop all services
docker-compose down

# Full restart
docker-compose down && docker-compose up -d
```

### Using Makefile Shortcuts

```bash
make docker-build      # Rebuild images
make docker-up         # Start services
make docker-down       # Stop services
make docker-logs       # View live logs
make docker-shell      # Jump into container
make docker-migrate    # Run migrations
make docker-superuser  # Create superuser
make docker-restart    # Full restart
make docker-clean      # Remove all containers & volumes
make docker-help       # Show all commands
```

## Environment Configuration

### `.env` File

Create `.env` from `.env.example`:

```bash
cp .env.example .env
```

**Key variables:**
- `DEBUG`: Set to `False` for production
- `SECRET_KEY`: Must be secret in production
- `DATABASE_URL`: Connection string (auto-configured for Docker)
- `ALLOWED_HOSTS`: Comma-separated list of allowed domains
- `SERVICE_API_TOKEN`: API token for special endpoints

### Production vs Development

**Development** (docker-compose.override.yml):
- `DEBUG=True`
- Django dev server
- Hot reload enabled
- Automatic superuser creation

**Production** (docker-compose.yml):
- `DEBUG=False`
- Gunicorn app server
- 4 workers, 120s timeout
- Manual secrets management

## Building & Publishing

### Build Image Locally

```bash
# Build from Dockerfile
docker-compose build

# Or with BuildKit (faster)
DOCKER_BUILDKIT=1 docker build -t pyauthservice:latest .
```

### View Image Size

```bash
docker images | grep pyauthservice
```

### Publish to Registry

```bash
# Tag image
docker tag pyauthservice:latest myregistry/pyauthservice:v1.0.0

# Push to registry (Docker Hub, ECR, etc)
docker push myregistry/pyauthservice:v1.0.0
```

## Database Management

### Backup Database

```bash
# Backup PostgreSQL
docker-compose exec db pg_dump -U authuser pyauthservice > backup.sql

# Or via docker
docker exec pyauthservice-db pg_dump -U authuser pyauthservice > backup.sql
```

### Restore Database

```bash
# Restore from backup
docker-compose exec -T db psql -U authuser pyauthservice < backup.sql
```

### Access Database CLI

```bash
docker-compose exec db psql -U authuser -d pyauthservice

# Inside psql:
# \dt                           # List tables
# SELECT * FROM users_user;     # Query users
# \q                            # Exit
```

## Troubleshooting

### "Port already in use"
```bash
# Change port in docker-compose.yml
# Change: "8000:8000"  to  "8001:8000"

docker-compose up -d
```

### "Database connection refused"
```bash
# Wait for database to start
sleep 10
docker-compose up -d

# Or check database logs
docker-compose logs db
```

### "Module not found"
```bash
# Rebuild to install new dependencies
docker-compose build
docker-compose up -d
```

### "Static files not found"
```bash
# Collect static files
docker-compose exec app python manage.py collectstatic --noinput
```

### Slow build
```bash
# Ensure .dockerignore is optimized
# Rebuild without cache
docker-compose build --no-cache
```

### Container exits immediately
```bash
# Check logs for errors
docker-compose logs app

# Try manual migration
docker-compose run --rm app python manage.py migrate
```

### Disk space issues
```bash
# Clean up unused Docker resources
docker system prune -a

# Remove stopped containers
docker container prune

# Remove unused volumes
docker volume prune
```

## Security Best Practices

### 1. Never Commit Secrets
✅ `.env` is in `.gitignore`  
❌ Don't add real secrets to `docker-compose.yml`

### 2. Use Strong Secrets
```bash
# Generate random secret
python -c "import secrets; print(secrets.token_urlsafe(50))"

# Add to .env
SECRET_KEY=<generated-value>
```

### 3. Limit Container Permissions
The app runs as non-root user `appuser` for security.

### 4. Keep Images Updated
```bash
# Pull latest base images
docker-compose build --pull
docker-compose up -d
```

### 5. Scan for Vulnerabilities
```bash
# If available
docker scan pyauthservice:latest
trivy image pyauthservice:latest
```

## Production Deployment

### AWS EC2 Deployment
See the [Docker Implementation Guide](https://github.com/ankithsajikumar/pyauthservice) for complete AWS EC2 setup:
- EC2 instance configuration
- Nginx reverse proxy
- SSL/HTTPS with Let's Encrypt
- GitHub Actions CI/CD
- Monitoring and backups

### Docker Swarm / Kubernetes
Modify `docker-compose.yml`:
- Add resource limits
- Add restart policies
- Configure health checks
- Use secrets management

### Health Checks
The Dockerfile includes health checks:
```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
    CMD python -c "import http.client; ..."
```

## Logs & Monitoring

### View Service Logs
```bash
docker-compose logs              # All services
docker-compose logs app          # App only
docker-compose logs -f app       # Follow app logs
docker-compose logs --tail=50    # Last 50 lines
```

### Monitor Resources
```bash
# CPU, Memory, Network usage
docker stats

# Container details
docker inspect pyauthservice-app
```

## Useful References

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/compose-file/)
- [Django Deployment](https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/gunicorn/)
- [PostgreSQL Docker](https://hub.docker.com/_/postgres)

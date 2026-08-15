.PHONY: docker-build docker-up docker-down docker-logs docker-shell docker-migrate docker-superuser docker-clean docker-restart


# Build Docker images
docker-build:
	docker-compose build

# Start containers
docker-up:
	docker-compose up -d
	@echo "✅ PyAuthService started!"
	@echo "🌐 Access at: http://localhost:8000"
	@echo "👨‍💼 Admin at: http://localhost:8000/admin"
	@echo "📚 API docs at: http://localhost:8000/api/"

# Stop containers
docker-down:
	docker-compose down

# View live logs
docker-logs:
	docker-compose logs -f app

# Jump into app container shell
docker-shell:
	docker-compose exec app bash

# Run database migrations manually (usually auto-runs)
docker-migrate:
	docker-compose exec app python manage.py migrate

# Create superuser
docker-superuser:
	docker-compose exec app python manage.py createsuperuser

# Full rebuild and restart
docker-restart:
	docker-compose down
	docker-compose build
	docker-compose up -d
	@echo "✅ PyAuthService restarted!"

# Clean up Docker resources
docker-clean:
	docker-compose down -v
	docker system prune -f
	@echo "✅ Docker cleanup complete"

# Run tests
docker-test:
	docker-compose exec app python manage.py test

# Format code
docker-format:
	docker-compose exec app black .
	docker-compose exec app isort .

# Check code quality
docker-lint:
	docker-compose exec app flake8

# View container resource usage
docker-stats:
	docker stats

# Help
docker-help:
	@echo "PyAuthService Docker Commands:"
	@echo "  make docker-build       - Build Docker images"
	@echo "  make docker-up          - Start containers"
	@echo "  make docker-down        - Stop containers"
	@echo "  make docker-logs        - View live logs"
	@echo "  make docker-shell       - Jump into app container"
	@echo "  make docker-migrate     - Run migrations manually"
	@echo "  make docker-superuser   - Create superuser"
	@echo "  make docker-restart     - Full rebuild and restart"
	@echo "  make docker-clean       - Clean all Docker resources"
	@echo "  make docker-test        - Run tests"
	@echo "  make docker-format      - Format code (black, isort)"
	@echo "  make docker-lint        - Check code quality (flake8)"
	@echo "  make docker-stats       - View container resource usage"
	@echo "  make docker-help        - Show this help message"

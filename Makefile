# Use uv instead of a virtualenv's pip
.PHONY: help lock-backend install-backend install-frontend setup run-dev stop lint test clean

help:
	@echo "Commands:"
	@echo "  setup          : Install all dependencies for backend and frontend."
	@echo "  lock-backend   : Generate requirements.txt from pyproject.toml using uv."
	@echo "  install-backend: Install backend dependencies from requirements.txt using uv."
	@echo "  install-frontend: Install frontend dependencies using npm."
	@echo "  run-dev        : Start all services using Docker Compose for development."
	@echo "  stop           : Stop all running Docker containers."
	@echo "  lint           : Run linters on the backend code using uv."
	@echo "  test           : Run tests for the backend using uv."
	@echo "  clean          : Remove temporary Python files and caches."

setup: install-backend install-frontend

lock-backend:
	@echo "Generating backend lockfile (requirements.txt)..."
	@cd backend && uv pip compile pyproject.toml -o requirements.txt

install-backend:
	@echo "Installing backend dependencies using uv..."
	@if [ ! -f backend/requirements.txt ]; then $(MAKE) lock-backend; fi
	@cd backend && uv pip sync requirements.txt

install-frontend:
	@echo "Installing frontend dependencies using npm..."
	@cd frontend && npm install

run-dev:
	@echo "Starting development environment with Docker Compose..."
	docker-compose -f docker-compose.dev.yml up -d --build

stop:
	@echo "Stopping all services..."
	docker-compose -f docker-compose.dev.yml down

lint:
	@echo "Running backend linters..."
	@cd backend && uv run ruff check . && uv run mypy .

test:
	@echo "Running backend tests..."
	@cd backend && uv run pytest

clean:
	@echo "Cleaning up..."
	@find . -type f -name "*.py[co]" -delete
	@find . -type d -name "__pycache__" -delete

delete:
	@echo "Deleting files from database..."
	docker exec -it intelliagent-db psql -U user -d intelliagent_db -c "DELETE FROM chunks; DELETE FROM documents;"

tests:
	@echo "Running tests..."
	docker compose -f docker-compose.dev.yml exec backend python -m pytest tests/ -v

celery:
	@echo "Starting Celery worker..."
	docker compose -f docker-compose.dev.yml exec backend celery -A workers.celery_app worker -l info --pool=solo

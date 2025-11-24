.PHONY: help install install-dev test lint format clean run docker-build docker-run migrate

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install production dependencies
	pip install -r requirements.txt

install-dev: ## Install development dependencies
	pip install -r requirements.txt -r requirements-dev.txt
	pre-commit install

test: ## Run tests with coverage
	pytest --cov=app --cov-report=html --cov-report=term-missing -v

test-watch: ## Run tests in watch mode
	ptw -- --cov=app --cov-report=term-missing

lint: ## Run all linting and formatting checks
	black --check app tests
	isort --check-only app tests
	flake8 app tests --max-line-length=100 --extend-ignore=E203,W503
	mypy app --ignore-missing-imports

format: ## Format code with black and isort
	black app tests
	isort app tests

security: ## Run security checks
	bandit -r app -f json -o bandit-report.json
	safety check

clean: ## Clean up cache and build files
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf htmlcov/ .coverage coverage.xml
	rm -rf dist/ build/
	rm -f *.db

run: ## Run the development server
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

docker-build: ## Build Docker image
	docker build -t task-manager-api:latest .

docker-run: ## Run Docker container
	docker run -d -p 8000:8000 --name task-manager-api \
		-e SECRET_KEY=your-secret-key-change-in-production \
		task-manager-api:latest

docker-compose-up: ## Start services with docker-compose
	docker-compose up -d

docker-compose-down: ## Stop services with docker-compose
	docker-compose down

docker-compose-logs: ## View docker-compose logs
	docker-compose logs -f

migrate-create: ## Create a new migration (use MESSAGE="your message")
	alembic revision --autogenerate -m "$(MESSAGE)"

migrate-up: ## Run pending migrations
	alembic upgrade head

migrate-down: ## Rollback last migration
	alembic downgrade -1

migrate-history: ## Show migration history
	alembic history

db-reset: ## Reset database (WARNING: deletes all data)
	rm -f *.db
	alembic upgrade head

setup: install-dev ## Setup development environment
	cp .env.example .env
	@echo "Please edit .env file with your configuration"

all: format lint test ## Run format, lint, and test

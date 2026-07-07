.PHONY: help install venv run dev migrate migration test lint format clean docker-up docker-down docker-logs

help:
	@echo "TaskFlowAPI - Available Commands:"
	@echo ""
	@echo "Setup & Installation:"
	@echo "  make install       - Install all dependencies"
	@echo "  make venv          - Create virtual environment"
	@echo ""
	@echo "Running Application:"
	@echo "  make run           - Start development server with auto-reload"
	@echo "  make migrate       - Run database migrations"
	@echo ""
	@echo "Development:"
	@echo "  make lint          - Run code linter (flake8)"
	@echo "  make format        - Format code with black"
	@echo "  make test          - Run tests with coverage"
	@echo ""
	@echo "Database:"
	@echo "  make migrate       - Run pending migrations"
	@echo "  make migration     - Create new migration"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-up     - Start PostgreSQL with Docker"
	@echo "  make docker-down   - Stop PostgreSQL container"
	@echo "  make docker-logs   - View PostgreSQL logs"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean         - Remove cache and build files"
	@echo ""

install:
	pip install -r requirements.txt
	@echo "✅ Dependencies installed"

venv:
	python -m venv .venv
	@echo "✅ Virtual environment created"
	@echo "Run: source .venv/bin/activate (Linux/Mac) or .venv\\Scripts\\activate (Windows)"

run: dev

dev:
	uvicorn main:app --reload --host 0.0.0.0 --port 8000

migrate:
	alembic upgrade head
	@echo "✅ Migrations applied"

migration:
	@read -p "Enter migration description: " desc; \
	alembic revision --autogenerate -m "$$desc"

lint:
	flake8 app/ --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 app/ --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
	pylint app/ --exit-zero
	@echo "✅ Linting complete"

format:
	black app/ --line-length 127
	isort app/
	@echo "✅ Code formatted"

test:
	pytest --cov=app tests/ -v
	@echo "✅ Tests completed"

docker-up:
	docker-compose up -d
	@echo "✅ PostgreSQL started"
	@echo "Wait 10 seconds for PostgreSQL to be ready..."
	sleep 10

docker-down:
	docker-compose down
	@echo "✅ PostgreSQL stopped"

docker-logs:
	docker-compose logs -f postgres

docker-clean:
	docker-compose down -v
	@echo "✅ PostgreSQL container and volumes removed"

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .coverage -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name htmlcov -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "✅ Cache cleaned"

.DEFAULT_GOAL := help

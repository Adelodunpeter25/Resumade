.PHONY: help install run dev test lint format clean migrate upgrade downgrade

help:
	@echo "Available commands:"
	@echo "  make install    - Install dependencies"
	@echo "  make run        - Run the application"
	@echo "  make dev        - Run in development mode with auto-reload"
	@echo "  make test       - Run tests"
	@echo "  make lint       - Run linting checks"
	@echo "  make format     - Format code with ruff"
	@echo "  make migrate    - Create a new migration"
	@echo "  make upgrade    - Apply migrations"
	@echo "  make downgrade  - Rollback last migration"
	@echo "  make clean      - Clean up cache and temp files"

install:
	pip install -r requirements.txt

run:
	uvicorn app.main:app --reload

dev:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
	pytest app/tests/ -v

lint:
	ruff check app/

format:
	ruff check --fix app/
	ruff format app/

migrate:
	@read -p "Enter migration message: " msg; \
	alembic revision --autogenerate -m "$$msg"

upgrade:
	alembic upgrade head

downgrade:
	alembic downgrade -1

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +

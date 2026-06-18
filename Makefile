.PHONY: help install dev build up down logs clean test lint migrate seed

help:
	@echo "Bookkeeping Platform - Available Commands"
	@echo "=========================================="
	@echo "Setup:"
	@echo "  make install      - Install dependencies"
	@echo "  make dev          - Start development environment"
	@echo "Development:"
	@echo "  make up           - Start Docker services"
	@echo "  make down         - Stop Docker services"
	@echo "  make logs         - View service logs"
	@echo "  make migrate      - Run database migrations"
	@echo "  make seed         - Seed sample data"
	@echo "Testing:"
	@echo "  make test         - Run tests"
	@echo "  make lint         - Run linters"
	@echo "Cleanup:"
	@echo "  make clean        - Clean up volumes and containers"

install:
	pip install -r requirements.txt
	cd frontend && npm install

dev:
	docker-compose up --build

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

logs-backend:
	docker-compose logs -f backend

logs-frontend:
	docker-compose logs -f frontend

logs-celery:
	docker-compose logs -f celery-worker

migrate:
	python -c "from backend.migrations import init_database; init_database()"

seed:
	python -c "from backend.migrations import seed_sample_data; seed_sample_data()"

test:
	pytest backend/test_api.py -v

lint:
	cd frontend && npm run lint

format:
	black backend/
	cd frontend && npm run format 2>/dev/null || true

clean:
	docker-compose down -v
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf frontend/.next
	rm -rf frontend/node_modules

health:
	curl -s http://localhost:8000/health | python -m json.tool

ps:
	docker-compose ps

restart:
	docker-compose restart

shell-backend:
	docker-compose exec backend /bin/bash

shell-postgres:
	docker-compose exec postgres psql -U bookkeeper -d bookkeeping

.PHONY: help build up down logs clean test

help:
	@echo "Available commands:"
	@echo "  make build       - Build all Docker images"
	@echo "  make up          - Start all services"
	@echo "  make down        - Stop all services"
	@echo "  make logs        - Show logs from all services"
	@echo "  make clean       - Remove all containers, volumes, and images"
	@echo "  make test        - Run backend tests"
	@echo "  make update-data - Trigger gamedata update"

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f

clean:
	docker compose down -v
	docker system prune -f

test:
	docker compose exec api pytest tests/ -v

update-data:
	docker compose exec api curl -X POST http://localhost:8000/gamedata/update


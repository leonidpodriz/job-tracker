build:
	@echo "Building docker images..."
	@docker compose build

up:
	@echo "Starting docker containers..."
	@docker compose up -d

down:
	@echo "Stopping docker containers..."
	@docker compose down

restart:
	@echo "Restarting docker containers..."
	@docker compose restart

logs:
	@echo "Showing docker logs..."
	@docker compose logs -f

migrate:
	@echo "Running migrations..."
	@docker compose run --rm --build app python manage.py migrate
	$(warning Database keeps running after migrations, execute 'make down' to stop it)

test:
	@echo "Running tests..."
	@docker compose run --rm --build app pytest

build-up: build up

.PHONY: build up down restart logs migrate build-up

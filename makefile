build:
	@echo "Building docker images..."
	@docker compose -f docker/compose-base.yml build

up:
	@echo "Starting docker containers..."
	@docker compose -f docker/compose-base.yml -f docker/compose-db.yml up -d

down:
	@echo "Stopping docker containers..."
	@docker compose -f docker/compose-base.yml -f docker/compose-db.yml down

restart:
	@echo "Restarting docker containers..."
	@docker compose -f docker/compose-base.yml -f docker/compose-db.yml restart

logs:
	@echo "Showing docker logs..."
	@docker compose -f docker/compose-base.yml -f docker/compose-db.yml logs -f

migrate:
	@echo "Running migrations..."
	@docker compose -f docker/compose-base.yml -f docker/compose-db.yml run --rm --build app python manage.py migrate
	$(warning Database keeps running after migrations, execute 'make down' to stop it)

test:
	@echo "Running tests..."
	@docker compose  -f docker/compose-base.yml  run --rm --build app pytest

format:
	@echo "Formatting code..."
	@docker compose  -f docker/compose-base.yml run --rm --build app black .

build-up: build up

.PHONY: build up down restart logs migrate build-up

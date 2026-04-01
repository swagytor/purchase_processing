PROJECT_NAME=purchase_processing
SERVICE_NAME=backend

up:
	docker compose -f docker-compose.yml -p $(PROJECT_NAME) up --remove-orphans
build:
	docker compose -f docker-compose.yml -p $(PROJECT_NAME) build --no-cache
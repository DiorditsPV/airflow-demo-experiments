include .env

DOCKER_COMPOSE = docker compose -f docker-compose.yaml
DOCKER = docker

.PHONY: help build up down restart logs init validate backup restore

help:
	@echo "Usage: make [build|up|down|restart|logs|init|validate|backup|restore]"

build:
	$(DOCKER_COMPOSE) build

up:
	$(DOCKER_COMPOSE) up -d

down:
	$(DOCKER_COMPOSE) down

restart: down up

logs:
	$(DOCKER_COMPOSE) logs -f


backup:
	$(DOCKER) exec postgres pg_dump -U $(DB_USER) $(DB_NAME) > backup/$(DB_NAME)_$(shell date +%Y%m%d_%H%M%S).sql


attach:
	$(DOCKER) exec -it airflow bash
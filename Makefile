DC = docker compose
COMPOSE_FILES = -f docker/app.yaml -f docker/storage.yaml -f docker/broker.yaml
ENV_FILE = --env-file .env
EXEC = docker exec -it
APP_CONTAINER = work_match_api

.PHONY: build start stop restart status clean

build:
	${DC} ${COMPOSE_FILES} ${ENV_FILE} up --build -d

start:
	${DC} ${COMPOSE_FILES} ${ENV_FILE} up -d

stop:
	${DC} ${COMPOSE_FILES} ${ENV_FILE} down

restart: stop start

status:
	${DC} ${COMPOSE_FILES} ${ENV_FILE} ps

clean:
	@read -p "This will remove all containers, networks, and volumes. Are you sure? [y/N]: " confirm && \
	if [ "$$confirm" = "y" ] || [ "$$confirm" = "Y" ]; then \
		${DC} ${COMPOSE_FILES} ${ENV_FILE} down -v; \
	else \
		echo "Aborted."; \
	fi

.PHONY: logs logs-app logs-errors

logs-app:
	${DC} ${COMPOSE_FILES} ${ENV_FILE} logs -f fastapi

logs:
	${DC} ${COMPOSE_FILES} ${ENV_FILE} logs -f

logs-errors:
	${DC} ${COMPOSE_FILES} ${ENV_FILE} logs 2>&1 | grep -i "error"

.PHONY: alembic-upgrade alembic-downgrade alembic-revision

alembic-upgrade:
	${EXEC} ${APP_CONTAINER} alembic upgrade head

alembic-downgrade:
	${EXEC} ${APP_CONTAINER} alembic downgrade -1

alembic-revision:
	${EXEC} ${APP_CONTAINER} alembic revision --autogenerate

.PHONY: test

test:
	${EXEC} ${APP_CONTAINER} pytest

.PHONY: generate-fake-data

generate-fake-data:
	${EXEC} ${APP_CONTAINER} python src/generate_fake_data.py

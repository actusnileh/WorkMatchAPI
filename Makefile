DC = docker compose
APP_FILE = docker/app.yaml
STORAGE_FILE = docker/storage.yaml
BROKER_FILE = docker/broker.yaml

ENV_FILE = --env-file .env
EXEC = docker exec -it
APP_CONTAINER = work_match_api

.PHONY: build
build:
	${DC} -f ${APP_FILE} -f ${STORAGE_FILE} -f ${BROKER_FILE} ${ENV_FILE} up --build -d

.PHONY: drop-all
drop-all:
	${DC} -f ${APP_FILE} -f ${STORAGE_FILE} -f ${BROKER_FILE} ${ENV_FILE}  down

.PHONY: logs-app
logs-app:
	${DC} -f ${APP_FILE} ${ENV_FILE}  logs -f

.PHONY: logs
logs:
	${DC} -f ${APP_FILE} -f ${STORAGE_FILE} -f ${BROKER_FILE} ${ENV_FILE}  logs -f

.PHONY: alembic-upgrade
alembic-upgrade:
	${EXEC} ${APP_CONTAINER} alembic upgrade head

.PHONY: alembic-downgrade
alembic-downgrade:
	${EXEC} ${APP_CONTAINER} alembic downgrade -1

.PHONY: alembic-revision
alembic-revision:
	${EXEC} ${APP_CONTAINER} alembic revision --autogenerate
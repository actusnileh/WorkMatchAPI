DC = docker compose
APP_FILE = docker/app.yaml
ENV_FILE = --env-file .env

.PHONY: build
build:
	${DC} -f ${APP_FILE} ${ENV_FILE} up --build -d

.PHONY: drop-all
drop-all:
	${DC} -f ${APP_FILE} ${ENV_FILE}  down

.PHONY: logs-app
logs-app:
	${DC} -f ${APP_FILE} ${ENV_FILE}  logs -f

.PHONY: logs
logs:
	${DC} -f ${APP_FILE} ${ENV_FILE}  logs -f
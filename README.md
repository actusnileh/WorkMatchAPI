
<h1 align="center" id="title">⚙️ WorkMatch API</h1>

<p align="center">
  <strong>WorkMatch API</strong> — современное backend-решение для управления вакансиями, пользователями и аналитикой в HR-системе.
</p>


## 🚀 Описание

WorkMatch API предоставляет удобный и расширяемый интерфейс для работы с моделями вакансий, пользователей, ролей и другими сущностями, а также интегрируется с брокерами и хранилищами данных.


## 📦 Установка и запуск

Чтобы развернуть проект локально, выполните следующие шаги:

1. **Клонируйте репозиторий:**

```bash
git clone https://github.com/actusnileh/WorkMatchAPI.git && cd WorkMatchAPI
```

2. **Убедитесь, что у вас установлены:**

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [GNU Make](https://www.gnu.org/software/make/)

3. **Создайте и настройте файл `.env`:**

В корне проекта найдите файл `.env.example` и скопируйте или переименуйте его в `.env`:
```env
PYTHON_PATH=src

API_PORT=8000
DEBUG_PORT=5678
ENVIRONMENT=development

POSTGRES_USER=user
POSTGRES_DB=database
POSTGRES_PASSWORD=password
POSTGRES_HOST=postgres
POSTGRES_PORT=6123

POSTGRES_DB_TEST=database_test

REDIS_URL=redis://work_match_api_redis:6379
ELASTICSEARCH_URL=http://work_match_api_elasticsearch:9200
CELERY_BROKER_URL=amqp://guest:guest@rabbitmq:5672
```

4. **Запустите проект с помощью Make:**

- Собрать и запустить контейнеры:

```bash
make build
```

- Запустить контейнеры (если они уже собраны):

```bash
make start
```

- Остановить все контейнеры:

```bash
make stop
```

- Перезапустить контейнеры:

```bash
make restart
```

- Проверить статус контейнеров:

```bash
make status
```

- Полностью удалить контейнеры, сети и тома:

```bash
make clean
```


## ⚙️ Основные команды Makefile

- `make logs` — Просмотр всех логов в режиме реального времени
- `make logs-app` — Просмотр логов приложения fastapi
- `make logs-errors` — Фильтрация логов с ошибками
- `make alembic-upgrade` — Выполнить миграции базы данных (upgrade head)
- `make alembic-downgrade` — Откатить миграцию базы данных на один шаг назад
- `make alembic-revision` — Создать новую миграцию (autogenerate)
- `make test` — Запустить тесты внутри контейнера приложения
- `make generate-fake-data` — Сгенерировать фейковые данные для тестирования


## 🛠️ Вклад в проект

Мы рады вашим предложениям и улучшениям! Чтобы внести изменения:

1. Форкните репозиторий.
2. Создайте новую ветку (`git checkout -b feature-branch`).
3. Внесите изменения и сделайте коммит (`git commit -m "Добавил новую функциональность"`).
4. Отправьте ветку на GitHub (`git push origin feature-branch`).
5. Создайте Pull Request.

---
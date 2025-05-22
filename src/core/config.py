from enum import Enum

from pydantic import ConfigDict, field_validator
from pydantic_settings import BaseSettings


class EnvironmentType(str, Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TEST = "test"


class BaseConfig(BaseSettings):
    model_config = ConfigDict(case_sensitive=True, env_file=".env", env_file_encoding="utf-8", extra="allow")


class Config(BaseConfig):
    ENVIRONMENT: str = EnvironmentType.DEVELOPMENT

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_DB_TEST: str

    POSTGRES_URL: str | None = None
    POSTGRES_URL_TEST: str | None = None

    REDIS_URL: str

    ELASTICSEARCH_URL: str

    CELERY_BROKER_URL: str
    NEURAL_SERVICE_URL: str = "http://192.168.1.55:8001"

    SECRET_KEY: str = "super-secret-key"
    JWT_ALGORITHM: str = "HS256"
    RELEASE_VERSION: str = "0.1"
    JWT_EXPIRE_MINUTES: int = 60 * 24

    @field_validator("POSTGRES_URL", mode="before")
    def assemble_postgres_url(cls, v, info):
        if v:
            return v

        data = info.data or {}

        user = data.get("POSTGRES_USER")
        password = data.get("POSTGRES_PASSWORD")
        host = data.get("POSTGRES_HOST")
        port = data.get("POSTGRES_PORT")
        db = data.get("POSTGRES_DB")

        if all([user, password, host, port, db]):
            return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}"

        raise ValueError("Incomplete test Postgres config")

    @field_validator("POSTGRES_URL_TEST", mode="before")
    def assemble_postgres_url_test(cls, v, info):
        if v:
            return v

        data = info.data or {}

        user = data.get("POSTGRES_USER")
        password = data.get("POSTGRES_PASSWORD")
        host = data.get("POSTGRES_HOST")
        port = data.get("POSTGRES_PORT")
        db = data.get("POSTGRES_DB_TEST")

        if all([user, password, host, port, db]):
            return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}"

        raise ValueError("Incomplete test Postgres config")


config: Config = Config()

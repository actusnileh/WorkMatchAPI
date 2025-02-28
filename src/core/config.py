from enum import Enum

from pydantic_settings import BaseSettings


class EnvironmentType(str, Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TEST = "test"


class BaseConfig(BaseSettings):
    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"


class Config(BaseConfig):
    DEBUG: int = 0
    ENVIRONMENT: str = EnvironmentType.DEVELOPMENT
    POSTGRES_URL: str
    SECRET_KEY: str = "super-secret-key"
    JWT_ALGORITHM: str = "HS256"
    RELEASE_VERSION: str = "0.1"
    JWT_EXPIRE_MINUTES: int = 60 * 24


config: Config = Config()

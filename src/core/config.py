from logging import config as logging_config

from pydantic import BaseSettings
from dotenv import find_dotenv

from core.logger import LOGGING

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):
    # Название проекта. Используется в Swagger-документации
    PROJECT_NAME: str = 'movies'

    # Настройки Redis
    REDIS_HOST: str = 'redis'
    REDIS_PORT: int = 6379
    REDIS_CACHE_EXP_SECS: int = 300

    # Настройки Elasticsearch
    ELASTIC_HOST: str = 'elasticsearch'
    ELASTIC_PORT: int = 9200

    jwt_secret_key: str = 'some_key'
    jwt_algorithm: str = 'HS256'


    class Config:
        env_file = find_dotenv()
        env_file_encoding = 'utf-8'


settings = Settings()

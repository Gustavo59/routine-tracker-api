import logging
import sys

from dotenv import load_dotenv
from pydantic import SecretStr
from pydantic.networks import PostgresDsn
from pydantic_settings import BaseSettings


class DBSettings(BaseSettings):
    DATABASE_URL: PostgresDsn


class Settings(DBSettings):
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(levelname)-8s %(asctime)s [%(name)s:%(lineno)d] %(message)s"
    JWT_SECRET: SecretStr = ""
    TOKEN_EXPIRATION_HOURS: int = 48


def _configure_logging(settings: Settings):
    logging.basicConfig(level=settings.LOG_LEVEL, format=settings.LOG_FORMAT, stream=sys.stdout)


def get_settings() -> Settings:
    load_dotenv()
    settings = Settings()
    _configure_logging(settings)
    return settings


def get_db_settings() -> DBSettings:
    load_dotenv()
    return DBSettings()

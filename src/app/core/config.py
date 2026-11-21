from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class Settings(BaseSettings):
    """Settings Class"""

    app_name: str = "Voice First Task Planner"
    environment: str = "development"
    debug: bool = False

    # database
    database_url: str = ""

    # logging
    db_engine_log_level: LogLevel = "WARNING"
    db_pool_log_level: LogLevel = "WARNING"
    psycopg_log_level: LogLevel = "WARNING"
    log_level: LogLevel = "DEBUG"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Return instance of Settings"""
    return Settings()

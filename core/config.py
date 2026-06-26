import os
from typing import Dict, Any, cast

from core.secret_manager import SecretManager
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    MONGO_DB_URI: str
    MONGO_DB_NAME: str = "NotificationEngineDB"

    EMAIL_FROM_NAME: str
    SMTP_EMAIL: str
    SMTP_PASSWORD: SecretStr
    SMTP_HOST: str
    SMTP_PORT: int = 465

    REDIS_HOST: str
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: SecretStr

    RABBITMQ_URL: str = "amqp://admin:admin123@localhost:5672/"
    MAIN_QUEUE: str = "main_queue"
    RETRY_QUEUE: str = "retry_queue"
    DEAD_LETTER_QUEUE: str = "dead_letter_queue"
    MAX_RETRIES: int = 5


class Config:
    def __init__(self):
        self.secret_manager = SecretManager()
        self._settings: Settings | None = None

    def load(self) -> Settings:
        secrets: Dict[str, str] = self.secret_manager.get_all()

        merged = dict(os.environ)
        merged.update(secrets)

        # 👇 IMPORTANT FIX
        self._settings = Settings(**cast(Dict[str, Any], merged))

        return self._settings

    @property
    def settings(self) -> Settings:
        if not self._settings:
            return self.load()
        return self._settings


config = Config()
settings = config.settings
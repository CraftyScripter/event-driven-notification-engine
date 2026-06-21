from pydantic_settings import BaseSettings
from typing import Dict
from .secret_manager import SecretManager
from pydantic import SecretStr


class Settings(BaseSettings):
    # DATABASE CONFIGURATION
    MONGO_DB_URI: str
    MONGO_DB_NAME: str = "NotificationEngineDB"

    # GMAIL API CONFIGURATION
    SMTP_EMAIL: str
    SMTP_PASSWORD: SecretStr
    SMTP_HOST: str
    SMTP_PORT: int = 465
    EMAIL_FROM_NAME: str

    # REDIS CONFIGURATION
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: SecretStr

    # RABBITMQ CONFIGURATION
    RABBITMQ_URL: str = "amqp://admin:admin123@localhost:5672/"
    QUEUE_NAME: str = "notifications"

    class Config:
        extra = "ignore"  # Ignore extra fields from Infisical

    @classmethod
    def load(cls):
        secret_manager = SecretManager()
        secrets_dict: Dict[str, str] = secret_manager.get_secrets()
        return cls(**secrets_dict)  # type: ignore


settings = Settings.load()


if __name__ == "__main__":
    print(settings.MONGO_DB_URI)
    print(settings.REDIS_HOST)
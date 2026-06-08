from pydantic_settings import BaseSettings
from typing import Any
from .secret_manager import SecretManager


class Settings(BaseSettings):
    # DATABASE CONFIGURATION
    MONGO_DB_URI: str
    MONGO_DB_NAME: str = "NotificationEngineDB"

    # GMAIL API CONFIGURATION
    SMTP_USER: str
    SMTP_PASSWORD: str
    SMTP_HOST: str
    SMTP_PORT: int = 587
    EMAIL_FROM_NAME: str

    # REDIS CONFIGURATION
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str



    @classmethod
    def load(cls):
        # This tells Pylance: "Trust me, I know exactly what this dictionary contains."
        infisical_secrets = SecretManager()
        infisical_secrets.connect()
        infisical_secrets.fetch_secrets()
        secrets_dict = infisical_secrets.get_secrets()
        # print(infisical_secrets)
        # for key, value in infisical_secrets.items():
        #     value = str(value)

        #     if len(value) > 3:
        #         masked_value = value[:3] + "*" * (len(value) - 3)
        #     else:
        #         masked_value = "*" * len(value)

        #     print(f"{key}: {masked_value}")

        # print("======================\n")
        return cls(**secrets_dict)  # type: ignore


settings = Settings.load()


if __name__ == "__main__":
    print(settings)

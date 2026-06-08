import os

from dotenv import load_dotenv
from infisical_sdk import InfisicalSDKClient

load_dotenv()


class SecretManager:
    def __init__(self):
        self.NOTIFICATION_MANAGER_CLIENT_ID: str|None = os.getenv("NOTIFICATION_MANAGER_CLIENT_ID")
        self.NOTIFICATION_MANAGER_CLIENT_SECRET: str|None = os.getenv("NOTIFICATION_MANAGER_CLIENT_SECRET")
        self.NOTIFICATION_MANAGER_PROJECT_ID: str|None = os.getenv("NOTIFICATION_MANAGER_PROJECT_ID")
        self.NOTIFICATION_MANAGER_ENVIRONMENT_SLUG: str|None = os.getenv("NOTIFICATION_MANAGER_ENVIRONMENT_SLUG")

        # Initialize the client
        self.client = InfisicalSDKClient(host="https://app.infisical.com")


    def connect(self):

        # Authenticate (example using Universal Auth)
        self.client.auth.universal_auth.login(
            client_id=self.NOTIFICATION_MANAGER_CLIENT_ID, # type: ignore
            client_secret=self.NOTIFICATION_MANAGER_CLIENT_SECRET, # type: ignore
        )

        
    
    def fetch_secrets(self):
        
        self.database_secrets = self.client.secrets.list_secrets(
            project_id=self.NOTIFICATION_MANAGER_PROJECT_ID,  # type: ignore
            environment_slug=self.NOTIFICATION_MANAGER_ENVIRONMENT_SLUG, # type: ignore
            secret_path="/",
        )
        self.email_secrets = self.client.secrets.list_secrets(
            project_id=self.NOTIFICATION_MANAGER_PROJECT_ID,  # type: ignore
            environment_slug=self.NOTIFICATION_MANAGER_ENVIRONMENT_SLUG, # type: ignore
            secret_path="/email/",
        )

        self.redis_secrets = self.client.secrets.list_secrets(
            project_id=self.NOTIFICATION_MANAGER_PROJECT_ID,  # type: ignore
            environment_slug=self.NOTIFICATION_MANAGER_ENVIRONMENT_SLUG, # type: ignore
            secret_path="/redis/",
        )
        

    def get_secrets(self):
        secrets_dict = dict()
        for secret in self.database_secrets.secrets:
            print(f"{secret.secretKey}: {secret.secretValue}")
            secrets_dict[secret.secretKey] = secret.secretValue

        for secret in self.email_secrets.secrets:
            print(f"{secret.secretKey}: {secret.secretValue}")
            secrets_dict[secret.secretKey] = secret.secretValue
        
        for secret in self.redis_secrets.secrets:
            print(f"{secret.secretKey}: {secret.secretValue}")
            secrets_dict[secret.secretKey] = secret.secretValue

        

        return secrets_dict



if __name__ == "__main__":
    secret_manager = SecretManager()
    secrets = secret_manager.get_secrets()
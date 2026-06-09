import os
import time
import logging
from typing import Dict, Optional, Any
from datetime import datetime, timedelta
from dotenv import load_dotenv
from infisical_sdk import InfisicalSDKClient

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SecretManager:
    def __init__(self, cache_ttl: int = 300, max_retries: int = 3):
        self.cache_ttl: int = cache_ttl
        self.max_retries: int = max_retries
        self._cache: Optional[Dict[str, str]] = None
        self._cache_time: Optional[datetime] = None
        
        # Config
        self.client_id: Optional[str] = os.getenv("NOTIFICATION_MANAGER_CLIENT_ID")
        self.client_secret: Optional[str] = os.getenv("NOTIFICATION_MANAGER_CLIENT_SECRET")
        self.project_id: Optional[str] = os.getenv("NOTIFICATION_MANAGER_PROJECT_ID")
        self.env_slug: Optional[str] = os.getenv("NOTIFICATION_MANAGER_ENVIRONMENT_SLUG")
        
        self.client: InfisicalSDKClient = InfisicalSDKClient(host="https://app.infisical.com")
    
    def _connect(self) -> None:
        """Connect with retry"""
        for attempt in range(self.max_retries):
            try:
                self.client.auth.universal_auth.login(
                    client_id=self.client_id,  # type: ignore
                    client_secret=self.client_secret,  # type: ignore
                )
                return
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise
                logger.warning(f"Retry {attempt + 1}: {e}")
                time.sleep(2 ** attempt)
    
    def _is_cache_valid(self) -> bool:
        if not self._cache or not self._cache_time:
            return False
        return (datetime.now() - self._cache_time).seconds < self.cache_ttl
    
    def _fetch_secrets(self) -> Dict[str, str]:
        """Fetch all secrets"""
        self._connect()
        
        secrets: Dict[str, str] = {}
        paths: list[str] = ["/", "/email/", "/redis/"]
        
        for path in paths:
            try:
                response = self.client.secrets.list_secrets(
                    project_id=self.project_id,  # type: ignore
                    environment_slug=self.env_slug,  # type: ignore
                    secret_path=path,
                )
                for secret in response.secrets:
                    secrets[secret.secretKey] = secret.secretValue
            except Exception as e:
                logger.error(f"Failed to fetch from {path}: {e}")
                raise
        
        return secrets
    
    def get_secrets(self, force_refresh: bool = False) -> Dict[str, str]:
        """Get all secrets with caching"""
        if not force_refresh and self._is_cache_valid() and self._cache is not None:
            logger.debug("Returning cached secrets")
            return self._cache
        
        logger.info("Fetching fresh secrets")
        self._cache = self._fetch_secrets()
        self._cache_time = datetime.now()
        return self._cache
    
    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Get specific secret"""
        secrets: Dict[str, str] = self.get_secrets()
        return secrets.get(key, default)


# Simple usage
if __name__ == "__main__":
    sm: SecretManager = SecretManager(cache_ttl=300, max_retries=3)
    
    # Get all secrets
    all_secrets: Dict[str, str] = sm.get_secrets()
    print(f"Loaded {len(all_secrets)} secrets")
    
    # Get specific secret
    db_password: Optional[str] = sm.get("DB_PASSWORD")
    print(f"DB Password: {db_password}")
    
    # Force refresh
    fresh: Dict[str, str] = sm.get_secrets(force_refresh=True)
    print(f"Refreshed {len(fresh)} secrets")
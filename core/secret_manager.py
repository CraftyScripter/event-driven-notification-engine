import os
import time
import threading
import logging
from typing import Dict, Optional

from dotenv import load_dotenv
from infisical_sdk import InfisicalSDKClient

load_dotenv()

logger = logging.getLogger(__name__)


class SecretManager:
    """
    Production-grade Infisical Secret Manager with:
    - In-memory caching
    - TTL-based refresh
    - Thread-safe locking
    - Background refresh support
    - Singleton-safe usage (recommended via instance)
    """

    def __init__(
        self,
        cache_ttl: int = 300,
        auto_refresh: bool = True,
        refresh_interval: int = 180,
        max_retries: int = 3,
    ):
        self.cache_ttl = cache_ttl
        self.refresh_interval = refresh_interval
        self.auto_refresh = auto_refresh
        self.max_retries = max_retries

        self._cache: Optional[Dict[str, str]] = None
        self._cache_time: float = 0.0

        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None

        # Infisical config
        self.client_id = os.getenv("NOTIFICATION_MANAGER_CLIENT_ID", "")
        self.client_secret = os.getenv("NOTIFICATION_MANAGER_CLIENT_SECRET", "")
        self.project_id = os.getenv("NOTIFICATION_MANAGER_PROJECT_ID", "")
        self.env_slug = os.getenv("NOTIFICATION_MANAGER_ENVIRONMENT_SLUG", "")

        self.client = InfisicalSDKClient(host="https://app.infisical.com")

        # connect once
        self._connect()

        # preload secrets at startup
        self.refresh()

        # start background refresh
        if self.auto_refresh:
            self._start_background_refresh()

    # -------------------------
    # Connection
    # -------------------------
    def _connect(self) -> None:
        for attempt in range(self.max_retries):
            try:
                self.client.auth.universal_auth.login(
                    client_id=self.client_id,
                    client_secret=self.client_secret,
                )
                logger.info("Infisical authenticated successfully")
                return
            except Exception as e:
                logger.warning(f"Auth retry {attempt + 1}: {e}")
                time.sleep(2 ** attempt)

        raise RuntimeError("Failed to authenticate with Infisical")

    # -------------------------
    # Cache validation
    # -------------------------
    def _is_cache_valid(self) -> bool:
        if not self._cache:
            return False
        return (time.time() - self._cache_time) < self.cache_ttl

    # -------------------------
    # Fetch secrets from Infisical
    # -------------------------
    def _fetch_secrets(self) -> Dict[str, str]:
        secrets: Dict[str, str] = {}

        paths = ["/", "/email/", "/redis/"]

        for path in paths:
            try:
                response = self.client.secrets.list_secrets(
                    project_id=self.project_id,
                    environment_slug=self.env_slug,
                    secret_path=path,
                )

                for secret in response.secrets:
                    secrets[secret.secretKey] = secret.secretValue

            except Exception as e:
                logger.error(f"Failed fetching secrets from {path}: {e}")
                raise

        return secrets

    # -------------------------
    # Refresh (thread-safe)
    # -------------------------
    def refresh(self) -> Dict[str, str]:
        with self._lock:
            # double-check inside lock (prevents stampede)
            if self._is_cache_valid():
                return self._cache  # type: ignore

            logger.info("Refreshing secrets from Infisical...")

            self._cache = self._fetch_secrets()
            self._cache_time = time.time()

            logger.info(f"Loaded {len(self._cache)} secrets")
            return self._cache

    # -------------------------
    # Get all secrets
    # -------------------------
    def get_all(self, force_refresh: bool = False) -> Dict[str, str]:
        if not force_refresh and self._is_cache_valid():
            return self._cache  # type: ignore

        return self.refresh()

    # -------------------------
    # Get single secret
    # -------------------------
    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        secrets = self.get_all()
        return secrets.get(key, default)

    # -------------------------
    # Manual invalidation
    # -------------------------
    def invalidate(self) -> None:
        with self._lock:
            self._cache = None
            self._cache_time = 0.0
            logger.warning("Secret cache invalidated")

    # -------------------------
    # Background refresh loop
    # -------------------------
    def _background_loop(self):
        while not self._stop_event.is_set():
            try:
                time.sleep(self.refresh_interval)
                self.refresh()
            except Exception as e:
                logger.error(f"Background refresh failed: {e}")

    def _start_background_refresh(self):
        self._thread = threading.Thread(
            target=self._background_loop,
            daemon=True,
        )
        self._thread.start()

    # -------------------------
    # Shutdown cleanup
    # -------------------------
    def stop(self):
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=5)
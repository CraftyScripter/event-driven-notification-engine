import logging
from typing import Optional
import redis.asyncio as aioredis

logger = logging.getLogger(__name__)

class RedisManager:
    def __init__(self, redis_url: str = "redis://localhost:6379/0"):
        self.redis_url = redis_url
        # Is client variable mein hum connection pool hold karenge
        self.client: Optional[aioredis.Redis] = None

    async def connect(self) -> None:
        """Initialize the Redis Connection Pool"""
        if not self.client:
            logger.info("Initializing Redis connection pool...")
            # decode_responses=True se data automatically string me convert ho jata hai
            self.client = aioredis.from_url(
                self.redis_url, 
                decode_responses=True,
                max_connections=10  # Optional: Connection pool ki limit set karne ke liye
            )
            # Connection check karne ke liye ping
            await self.client.ping()
            # logger.info("Redis connected successfully.")

    async def disconnect(self) -> None:
        """Close the Redis Connection Pool"""
        if self.client:
            logger.info("Closing Redis connection pool...")
            await self.client.close()
            self.client = None
            logger.info("Redis connection closed.")
    
    async def get_client(self) -> aioredis.Redis:
        """Redis client ko access karne ke liye method"""
        if not self.client:
            raise RuntimeError("Redis client is not connected. Call connect() first.")
        return self.client

    # --- Ab yahan aap apne custom methods bana sakte hain ---

    async def set_cache(self, key: str, value: str, expire_seconds: int = 300) -> bool:
        """Data cache karne ke liye wrapper method"""
        if not self.client:
            raise RuntimeError("Redis client is not connected.")
        try:
            await self.client.set(key, value, ex=expire_seconds)
            return True
        except Exception as e:
            logger.error(f"Redis SET error for key {key}: {e}")
            return False

    async def get_cache(self, key: str) -> Optional[str]:
        """Data fetch karne ke liye wrapper method"""
        if not self.client:
            raise RuntimeError("Redis client is not connected.")
        try:
            return await self.client.get(key)
        except Exception as e:
            logger.error(f"Redis GET error for key {key}: {e}")
            return None

# Ek single instance create karke export karenge (Singleton Pattern)
redis_manager = RedisManager()
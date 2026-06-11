from redis.asyncio import Redis
import logging

logger = logging.getLogger(__name__)

class IdempotencyService:
    # Constructor Dependency Injection
    def __init__(self, redis_client: Redis, expiry_seconds: int = 86400):
        self.redis_client = redis_client
        self.expiry_seconds = expiry_seconds

    async def is_processed(self, event_id: str) -> bool:
        try:
            exists = await self.redis_client.exists(f"idempotency:{event_id}")
            return bool(exists)
        except Exception as e:
            logger.error(f"Redis error in is_processed for {event_id}: {e}")
            return False

    async def mark_processed(self, event_id: str):
        try:
            await self.redis_client.setex(
                name=f"idempotency:{event_id}",
                time=self.expiry_seconds,
                value="processed"
            )
        except Exception as e:
            logger.error(f"Failed to mark event {event_id} as processed in Redis: {e}")
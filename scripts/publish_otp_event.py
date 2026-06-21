
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

import json
from datetime import datetime
from uuid import uuid4
import aio_pika

# from core.config import settings
RABBITMQ_URL = "amqp://admin:admin123@localhost:5672/"
QUEUE_NAME = "notifications"


async def main():
    connection = await aio_pika.connect_robust(
        RABBITMQ_URL
    )

    async with connection:
        channel = await connection.channel()

        queue = await channel.declare_queue(
            QUEUE_NAME,
            durable=True,
        )

        event = {
            "event_id": str(uuid4()),
            "event_type": "auth.otp_sent",
            "timestamp": datetime.now().isoformat(),
            "source": "auth-service",
            "data": {
                "channel": "email",
                "recipient": "anujkcontactme122003@gmail.com",
                "otp": "123456",
            },
        }

        await channel.default_exchange.publish(
            aio_pika.Message(
                body=json.dumps(event).encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            ),
            routing_key=queue.name,
        )

        print("Event Published")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
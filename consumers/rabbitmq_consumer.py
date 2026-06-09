from events.schemas.base import BaseEvent
from events.registry import get_event_config
import aio_pika
from core import settings
from notifications.service import NotificationService
import json

class RabbitMQConsumer:
    """
    Responsible for processing incoming RabbitMQ messages.

    This class does not know anything about SMS, Email,
    OTP business logic, etc.

    It only:
        1. Validates events
        2. Resolves handlers
        3. Executes handlers
    """

    def __init__(self, notification_service: NotificationService) -> None:
        self.notification_service = (notification_service)

    async def start(self) -> None:
        connection = await aio_pika.connect_robust(
            settings.RABBITMQ_URL
        )

        channel = await connection.channel()

        await channel.set_qos(
            prefetch_count=10
        )

        queue = await channel.declare_queue(
            settings.QUEUE_NAME,
            durable=True,
        )

        async with queue.iterator() as queue_iter:

            async for message in queue_iter:

                async with message.process():

                    payload = json.loads(
                        message.body.decode()
                    )

                    await self.process_message(
                        payload
                    )

    async def process_message(
        self,
        payload: dict,
    ) -> None:
        """
        Process a single RabbitMQ message.
        """

        # Step 1
        # Validate common event fields.
        base_event = BaseEvent.model_validate(payload)

        # Step 2
        # Find schema + handler from registry.
        event_config = get_event_config(
            base_event.event_type
        )

        if event_config is None:
            raise ValueError(
                f"Unsupported event type: {base_event.event_type}"
            )

        # Step 3
        # Validate event against its schema.
        event_schema = event_config["schema"]

        validated_event = event_schema.model_validate(
            payload
        )

        # Step 4
        # Create handler.
        handler_cls = event_config["handler"]

        handler = handler_cls(
            notification_service=self.notification_service
        )

        # Step 5
        # Execute handler.
        await handler.handle(
            validated_event
        )
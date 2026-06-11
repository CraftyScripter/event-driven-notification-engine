"""
RabbitMQ Consumer Module

This module provides a consumer service for processing incoming RabbitMQ messages
asynchronously. It handles event validation, routing, and execution of appropriate
handlers based on event types.
"""

from events.schemas.base import BaseEvent
from events.registry import get_event_config
import aio_pika
from core import settings
from notifications.service import NotificationService
import json


class RabbitMQConsumer:
    """
    Responsible for processing incoming RabbitMQ messages.

    This class follows the Single Responsibility Principle and maintains separation
    of concerns by only handling message consumption, validation, and routing.
    It does NOT contain any business logic related to:
        - SMS sending
        - Email delivery
        - OTP generation or verification
        - Any other notification-specific operations

    Responsibilities:
        1. Establish and manage RabbitMQ connection
        2. Receive messages from the queue
        3. Validate event structure and data
        4. Resolve appropriate event handlers from registry
        5. Execute handlers with validated events
        6. Handle message acknowledgment (via context manager)

    The actual business logic is delegated to specific event handlers that are
    resolved from the event registry.
    """

    def __init__(self, notification_service: NotificationService) -> None:
        """
        Initialize the RabbitMQ consumer with a notification service.

        The notification service is injected as a dependency and will be passed
        to individual event handlers for their operations.

        Args:
            notification_service (NotificationService): Service instance that
                handles notification-related operations (email, SMS, etc.).
                This service is shared across all event handlers.

        Example:
            notification_service = NotificationService()
            consumer = RabbitMQConsumer(notification_service)
        """
        self.notification_service = notification_service

    async def start(self) -> None:
        """
        Start consuming messages from the RabbitMQ queue.

        This method establishes a connection to RabbitMQ, creates a channel,
        sets prefetch limits, declares the queue, and begins an infinite loop
        of message consumption.

        Workflow:
            1. Establishes robust connection to RabbitMQ broker
            2. Creates a communication channel
            3. Sets QoS (Quality of Service) to limit concurrent message processing
            4. Declares/connects to the target queue (creates if doesn't exist)
            5. Iterates through incoming messages
            6. For each message, processes it and automatically acknowledges
               (via context manager) when done

        Note:
            - Uses connection pooling and automatic reconnection via connect_robust()
            - Messages are automatically acknowledged after successful processing
            - Prefetch count of 10 prevents overwhelming the consumer
            - Queue is durable (survives broker restarts)

        Raises:
            aio_pika.exceptions.AMQPConnectionError: If connection to RabbitMQ fails
            json.JSONDecodeError: If message body contains invalid JSON
            Exception: Any error during message processing
        """
        # Establish robust connection with automatic reconnection
        connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)

        # Create a channel for communication
        channel = await connection.channel()

        # Limit number of unacknowledged messages to prevent overload
        # This ensures fair distribution across consumers
        await channel.set_qos(prefetch_count=10)

        # Declare queue (creates if not exists)
        # Durable=True ensures queue survives broker restart
        queue = await channel.declare_queue(settings.QUEUE_NAME, durable=True)

        # Iterate through messages indefinitely
        # The async context manager handles message acknowledgment automatically
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                # process() context manager automatically acknowledges message
                # when exiting successfully, or rejects on exception
                async with message.process():
                    # Parse JSON payload from message body
                    payload = json.loads(message.body.decode())

                    # Process the validated payload
                    await self.process_message(payload)

    async def process_message(self, payload: dict) -> None:
        """
        Process a single RabbitMQ message through the event pipeline.

        This method implements a multi-step pipeline for event processing:
            1. Basic validation of common event fields
            2. Lookup event configuration from registry
            3. Full schema validation of event-specific data
            4. Handler instantiation
            5. Handler execution

        The pipeline ensures that only valid, well-structured events reach
        the business logic handlers.

        Args:
            payload (dict): Decoded JSON message payload containing event data.
                Must include at minimum an 'event_type' field.

        Raises:
            ValueError: If the event type is not supported or registered.
            ValidationError: If payload fails schema validation (from Pydantic).
            Exception: Any error from handler execution.

        Example payload:
            {
                "event_type": "user.registered",
                "user_id": "12345",
                "email": "user@example.com",
                "timestamp": "2024-01-01T12:00:00Z"
            }

        Pipeline Steps:
            Step 1: Validate common fields (event_type, etc.)
            Step 2: Find handler and schema in registry
            Step 3: Validate against specific event schema
            Step 4: Create handler instance with notification service
            Step 5: Execute handler with validated event
        """
        # ===== STEP 1: Basic Common Validation =====
        # Validate only the common fields that all events share.
        # This gives us the event_type to look up the specific configuration.
        base_event = BaseEvent.model_validate(payload)

        # ===== STEP 2: Registry Lookup =====
        # Find the specific schema and handler for this event type.
        # Registry maps event_type strings to their configurations.
        event_config = get_event_config(base_event.event_type)

        if event_config is None:
            # Event type not registered - this is a critical error
            raise ValueError(f"Unsupported event type: {base_event.event_type}")

        # ===== STEP 3: Full Schema Validation =====
        # Validate the complete payload against the event-specific schema.
        # This ensures all required fields for this event type are present
        # and correctly formatted.
        event_schema = event_config["schema"]
        validated_event = event_schema.model_validate(payload)

        # ===== STEP 4: Handler Instantiation =====
        # Create the event handler instance, injecting the notification service.
        # Handlers are stateless and can be created per message.
        handler_cls = event_config["handler"]
        handler = handler_cls(notification_service=self.notification_service)

        # ===== STEP 5: Handler Execution =====
        # Execute the handler's business logic with the validated event.
        # This is where actual notification operations (SMS, email, etc.) occur.
        await handler.handle(validated_event)
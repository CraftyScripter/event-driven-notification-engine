# /events/schemas/base.py
"""base.py
-------------
Defines the BaseEvent schema that all incoming events must follow.
This ensures a consistent contract for the notification service regardless of event type.
"""

from datetime import datetime
from typing import Any
from pydantic import BaseModel, Field
from core import EventType


class BaseEvent(BaseModel):
    event_id: str = Field(
        description="Unique identifier for the event"
    )

    event_type: EventType = Field(  # String ki jagah Enum use kiya
        description="Type of event (otp, order_created, etc.)"
    )

    timestamp: datetime = Field(
        description="When the event was generated"
    )

    source: str = Field(
        description="Name of the producer service (e.g., 'auth-service', 'order-service')"
    )

    data: dict[str, Any] = Field(
        description="Business payload (e.g., {'email': 'abc@xyz.com', 'otp_code': '1234'})"
    )
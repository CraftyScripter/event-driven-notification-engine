from typing import Any
from pydantic import BaseModel, Field, model_validator

from .base import BaseEvent, EventType
from core import NotificationChannel


class OTPData(BaseModel):
    """
    Business payload for OTP notifications.
    """
    channel: NotificationChannel = Field(
        description="Notification channel (email, sms, etc.)"
    )
    recipient: str = Field(
        description="Phone number or email address"
    )
    otp: str = Field(
        description="One time password"
    )


class OTPEvent(BaseEvent):
    """
    Schema representing an OTP event with strict validation.
    """
    data: OTPData

    # @model_validator(mode="before")
    # @classmethod
    # def validate_event_type(cls, data: Any) -> Any:
    #     """
    #     Strictly validate event_type across dict, objects, or attributes.
    #     """
    #     event_type = None

    #     # Case 1: If the incoming data is a raw dictionary (e.g., JSON)
    #     if isinstance(data, dict):
    #         event_type = data.get("event_type")
            
    #     # Case 2: If the incoming data is another Pydantic model or an object
    #     elif hasattr(data, "event_type"):
    #         event_type = getattr(data, "event_type")
            
    #     else:
    #         raise ValueError("Invalid data format for OTPEvent validation.")

    #     # Final Strict Check: Unified validation for both cases.
    #     # Extracting .value ensures smooth comparison for both Enums and Strings.
    #     actual_value = event_type.value if isinstance(event_type, EventType) else event_type
        
    #     if actual_value != "auth.otp_sent":
    #         raise ValueError("Invalid event_type for OTPEvent. Must be 'auth.otp_sent'.")

    #     return data
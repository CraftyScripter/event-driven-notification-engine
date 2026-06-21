from typing import Any
from pydantic import BaseModel, Field

from .base import BaseEvent
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

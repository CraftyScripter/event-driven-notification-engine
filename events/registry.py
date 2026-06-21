from core import EventType

from events import OTPEvent
from events.handlers.otp_handler import OTPEventHandler


EVENT_REGISTRY = {
    EventType.AUTH_OTP_SENT: {
        "schema": OTPEvent,
        "handler": OTPEventHandler,
        "template": "otp"
    }
}

def get_event_config(event_type: EventType):
    return EVENT_REGISTRY.get(event_type)
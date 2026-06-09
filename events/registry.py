from core import EventType

from events import OTPEvent
from events import OTPEventHandler


EVENT_REGISTRY = {
    EventType.AUTH_OTP_SENT: {
        "schema": OTPEvent,
        "handler": OTPEventHandler,
    }
}

def get_event_config(event_type: EventType):
    return EVENT_REGISTRY.get(event_type)
from enum import Enum



class NotificationChannel(str, Enum):
    """Enum representing supported notification channels."""

    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"
    WHATSAPP = "whatsapp"


class EventType(str, Enum):
    """
    Supported event types.
    """

    # Authentication
    AUTH_OTP_SENT = "auth.otp_sent"
    AUTH_PASSWORD_RESET_REQUESTED = "auth.password_reset_requested"
    AUTH_USER_REGISTERED = "auth.user_registered"

    # Orders
    ORDER_CREATED = "order.created"
    ORDER_SHIPPED = "order.shipped"

    # Payments
    PAYMENT_COMPLETED = "payment.completed"

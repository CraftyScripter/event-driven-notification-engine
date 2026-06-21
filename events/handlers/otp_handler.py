from notifications.service import NotificationService
from events.schemas.otp import OTPEvent
from events.handlers.base import BaseEventHandler
from core.enums import NotificationChannel

class OTPEventHandler(BaseEventHandler):

    def __init__(
        self,
        notification_service: NotificationService,
    ) -> None:
        self.notification_service = notification_service

    async def handle(
        self,
        event: OTPEvent,
    ) -> None:

        subject = None
        print(f"Handling OTPEvent for recipient: {event.data.recipient}, channel: {event.data.channel}")

        if event.data.channel == NotificationChannel.EMAIL:
            subject = "OTP Verification"

        await self.notification_service.process(
            template_name="otp",
            channel=event.data.channel,
            recipient=event.data.recipient,
            context=event.data.model_dump(),
            subject=subject,
        )
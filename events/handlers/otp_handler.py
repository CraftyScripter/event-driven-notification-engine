from events import OTPEvent
from notifications import NotificationService
from .base import BaseEventHandler


class OTPEventHandler(BaseEventHandler):

    def __init__(self, notification_service: NotificationService) -> None:
        self.notification_service = notification_service

    async def handle(
        self,
        event: OTPEvent,
    ) -> None:

        await self.notification_service.send_otp(
            event=event
        )
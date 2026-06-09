from core.enums import NotificationChannel

from notifications.providers.sms_provider import SMSProvider
from events.schemas.otp import OTPEvent


class NotificationService:
    """
    Service responsible for routing notifications
    to the appropriate provider.
    """

    def __init__(self) -> None:
        self.providers = {
            NotificationChannel.SMS: SMSProvider(),
        }
        print(self.providers)

    async def send_otp(
        self,
        event: OTPEvent,
    ) -> None:
        """
        Process OTP notification request
        and route it to the correct provider.
        """

        provider = self.providers.get(event.data.channel)

        if provider is None:
            raise ValueError(
                f"Unsupported notification channel: {event.data.channel}"
            )

        message = f"Your OTP is {event.data.otp}"

        await provider.send(
            recipient=event.data.recipient,
            message=message,
        )
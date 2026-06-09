from notifications.providers.base import NotificationProvider


class SMSProvider(NotificationProvider):
    """
    SMS notification provider.

    Phase 1:
    This provider only logs/prints the notification
    instead of sending a real SMS.
    """

    async def send(
        self,
        recipient: str,
        message: str,
    ) -> None:
        """
        Send SMS notification.

        Currently acts as a mock provider.
        """

        print(
            f"""
            ==========================
            SMS Notification
            ==========================
            Recipient: {recipient}
            Message: {message}
            ==========================
            """
        )
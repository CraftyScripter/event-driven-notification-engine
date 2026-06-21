from notifications.providers.base import NotificationProvider

class SMSProvider(NotificationProvider):
    """
    SMS notification provider.
    """

    async def send(self, recipients: list[str], content: str, **kwargs) -> None:
        # SMS ko sirf recipients aur content chahiye, baaki sab kwargs me pada rahega
        for recipient in recipients:
            print(
                f"""
                ==========================
                SMS Notification
                ==========================
                Recipient: {recipient}
                Message: {content}
                ==========================
                """
            )
from core import NotificationChannel
from notifications.providers.sms_providers.simple_sms_provider import SMSProvider
from notifications.providers.email_provider.simple_mail_provider import SimpleMailProvider

class ProviderManager:

    def __init__(self) -> None:
        self.providers = {
            NotificationChannel.SMS: [
                SMSProvider()
            ],
            NotificationChannel.EMAIL: [
                SimpleMailProvider()
            ]
        }

    async def send(
        self,
        *,
        channel: NotificationChannel,
        recipients: list[str],
        content: str,
        **kwargs,  # <--- Sabhi optional variables (subject, is_html, background_tasks) yahan aayenge
    ) -> None:

        providers = self.providers.get(channel, [])

        if not providers:
            raise ValueError(f"No provider configured for {channel}")

        print(f"ProviderManager: Sending notification via {channel} to {recipients}")
        last_error = None

        for provider in providers:
            try:
                print(f"ProviderManager: Testing provider: {provider.__class__.__name__}")

                # Humne recipients aur content ke sath baki saare optional arguments (**kwargs) aage bhej diye
                await provider.send(
                    recipients=recipients,
                    content=content,
                    **kwargs  # <--- Poora dabba aage pass ho gaya!
                )
                print(f"ProviderManager: Successfully sent notification via {provider.__class__.__name__}")
                return

            except Exception as exc:
                print(f"ProviderManager: Error using {provider.__class__.__name__}: {exc}")
                last_error = exc

        raise last_error # type: ignore
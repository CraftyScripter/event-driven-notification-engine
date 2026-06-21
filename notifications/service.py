# notifications/service.py

from core.enums import NotificationChannel
from notifications.template_engine import (
    TemplateEngine,
)
from notifications.provider_manager import (
    ProviderManager,
)

from events.schemas.otp import OTPEvent


class NotificationService:

    def __init__(
        self,
        template_engine: TemplateEngine,
        provider_manager: ProviderManager,
    ) -> None:

        self.template_engine = template_engine
        self.provider_manager = provider_manager


    async def process(
        self,
        *,
        template_name: str,
        channel: NotificationChannel,
        recipient: str,
        context: dict,
        subject: str | None = None,
    ) -> None:
        print(f"NotificationService: Processing notification for recipient: {recipient}, channel: {channel}, template: {template_name}")

        content = await self.template_engine.render(
            template_name=template_name,
            channel=channel,
            context=context
        )

        print(f"NotificationService: Generated content: {content}")

        await self.provider_manager.send(
            channel=channel,
            recipients=[recipient],
            content=content,
            subject=subject
        )
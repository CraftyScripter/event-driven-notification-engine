# notifications/template_engine.py



from tempfile import template
from pathlib import Path
from jinja2 import (
    Environment,
    FileSystemLoader,
)

from core.enums import NotificationChannel


TEMPLATE_EXTENSIONS = {
    NotificationChannel.SMS: "txt",
    NotificationChannel.WHATSAPP: "txt",
    NotificationChannel.EMAIL: "html",
}

class TemplateEngine:

    def __init__(self) -> None:

        template_dir = (
            Path(__file__).parent / "templates"
        )

        print(f"Template dir: {template_dir}")

        self.env = Environment(
            loader=FileSystemLoader(str(template_dir))
        )

    async def render(
        self,
        template_name: str,
        channel: NotificationChannel,
        context: dict,
    ) -> str:
        print(f"TemplateEngine: Rendering template: {template_name}, channel: {channel}")
        
        extension = TEMPLATE_EXTENSIONS[channel]

        template_path = (
            f"{template_name}/{channel.value}.{extension}"
        )
        print(f"template path: {template_path}")

        try:
            template = self.env.get_template(template_path)
        except Exception as e:
            print(type(e))
            print(e)
            raise
        print(f"TemplateEngine: Template loaded: {template}")
        print(f"TemplateEngine: Template rendered: {template.render(**context)}")

        return template.render(**context)
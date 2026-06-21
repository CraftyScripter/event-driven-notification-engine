from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType, NameEmail
from core.config import settings
from notifications.providers.base import NotificationProvider

class SimpleMailProvider(NotificationProvider):

    def __init__(self) -> None:
        self.conf = ConnectionConfig(
            MAIL_USERNAME = settings.SMTP_EMAIL,
            MAIL_PASSWORD = settings.SMTP_PASSWORD,
            MAIL_FROM = settings.SMTP_EMAIL,          
            MAIL_FROM_NAME = settings.EMAIL_FROM_NAME, 
            MAIL_PORT = settings.SMTP_PORT,
            MAIL_SERVER = settings.SMTP_HOST,
            MAIL_STARTTLS = False, # Port 587 ke liye settings se True/False manage karein
            MAIL_SSL_TLS = True,   # Port 465 ke liye True
            USE_CREDENTIALS = True,
            VALIDATE_CERTS = True
        )
        self.fm = FastMail(self.conf)

    async def send(self, recipients: list[NameEmail], content: str, **kwargs) -> dict:
        # Kwargs se Email specific fields nikal lo, aur default values set kar do
        subject = kwargs.get("subject") or "No Subject"
        is_html = kwargs.get("is_html", True)
        background_tasks = kwargs.get("background_tasks", None)

        subtype = MessageType.html if is_html else MessageType.plain

        # Message schema me humne 'content' ko 'body' me map kar diya
        message = MessageSchema(
            subject=subject,
            recipients=recipients, # fastapi-mail direct strings ki list accept karta hai
            body=content,
            subtype=subtype
        )

        if background_tasks:
            background_tasks.add_task(self.fm.send_message, message)
            return {"status": "queued", "message": "Email is being sent in the background"}
        else:
            await self.fm.send_message(message)
            return {"status": "sent", "message": "Email sent successfully"}
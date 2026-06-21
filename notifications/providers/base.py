from abc import ABC, abstractmethod

class NotificationProvider(ABC):
    @abstractmethod
    async def send(self, recipients: list[str], content: str, **kwargs) -> None:
        """
        Har provider is method ko implement karega.
        Extra arguments (subject, is_html, etc.) **kwargs me milenge.
        """
        pass
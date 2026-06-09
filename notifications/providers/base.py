from abc import ABC, abstractmethod
from typing import Any

class NotificationProvider(ABC):

    """
    Abstract base class for notification providers.
    This class defines the interface that all notification providers must implement.
    """


    @abstractmethod
    def send(self, recipient: str, message: str) -> None:
        """
        Send a notification based on the provided event data.
        """
        pass

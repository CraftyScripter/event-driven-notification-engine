from abc import ABC, abstractmethod

from events import OTPEvent


class BaseEventHandler(ABC):
    """
    Base contract for all event handlers.

    Every handler in the system must implement
    the handle() method.
    """

    @abstractmethod
    async def handle(self, event: OTPEvent) -> None:
        """
        Process an incoming event.
        """
        pass
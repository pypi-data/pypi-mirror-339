from typing import Any
from abc import ABC, abstractmethod
from ..lib import Event

class BackendNotSuppoortPatternMatching(Exception):
    pass

class PubSubBackendInterface(ABC):
    support_pattern_matching: bool = False
    
    @abstractmethod
    async def connect(self) -> None:
        """Connect to the pub/sub system"""
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        """Disconnect from the pub/sub system"""
        pass

    @abstractmethod
    async def publish(self, channel: str, message: Any) -> None:
        """Publish a message to a topic"""
        pass

    @abstractmethod
    async def subscribe(self, channel: str) -> None:
        """Subscribe to a channel"""
        pass

    async def psubscribe(self, channel_pattern: str) -> None:
        """Subscribe to channels according to pattern"""
        raise BackendNotSuppoortPatternMatching()

    @abstractmethod
    async def unsubscribe(self, channel: str) -> None:
        """Unsubscribe from a channel"""
        pass

    async def punsubscribe(self, channel_pattern: str) -> None:
        """Subscribe to channels according to pattern"""
        raise BackendNotSuppoortPatternMatching()

    @abstractmethod
    async def next_published(self) -> Event:
        pass

from __future__ import annotations

import asyncio
from typing import Optional, Any

from ..lib import Event
from .lib import PubSubBackendInterface


class InMemoryPubSubBackend(PubSubBackendInterface):
    def __init__(self, _url: Optional[str] = None):
        self._subscribed: set[str] = set()

    async def connect(self) -> None:
        self._published: asyncio.Queue[Event] = asyncio.Queue()

    async def disconnect(self) -> None:
        pass

    async def subscribe(self, channel: str) -> None:
        self._subscribed.add(channel)

    async def unsubscribe(self, channel: str) -> None:
        self._subscribed.remove(channel)

    async def publish(self, channel: str, message: Any) -> None:
        event = Event(channel=channel, data=message)
        await self._published.put(event)

    async def next_published(self) -> Event:
        while True:
            event = await self._published.get()
            if event.channel in self._subscribed:
                return event

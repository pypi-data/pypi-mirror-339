import redis.asyncio as aioredis
import asyncio
from typing import Any, Set
from loguru import logger
from ..lib import Event

from .lib import PubSubBackendInterface

class RedisPubSubBackend(PubSubBackendInterface):
    """
    Redis PubSub Manager that handles Redis pub/sub communication.

    Implemented as a singleton.
    Uses asyncio.Queue to bridge Redis messages to application code.


    NOTE
    psubscribe("channel:*") and then unsubscribe/punsubscribe("channel:1")
    won't stop listening `channel:1` unless you do exactly punsubscribe("channel:*")
    """

    conn: aioredis.Redis
    support_pattern_matching: bool = True
    
    def __init__(self, url: str, msg_queue_max_size: int = 10000):
        self._url = url;
        self.conn = aioredis.Redis.from_url(url, health_check_interval=30)
        self._pubsub = self.conn.pubsub(ignore_subscribe_messages=True)
        self._ready = asyncio.Event()
        self._listener: asyncio.Task[None] | None = None
        self._queue: asyncio.Queue[Event] = asyncio.Queue(maxsize=msg_queue_max_size)
        self._subscribed_channels: Set[str] = set()
        self._subscribed_patterns: Set[str] = set()

    async def connect(self) -> None:
       self._listener = asyncio.create_task(self._pubsub_listener())
       await self._pubsub.connect()
       logger.info(f"Connected to Redis at {self._url}.")

    async def disconnect(self) -> None:
        await self._pubsub.aclose()
        await self.conn.aclose()
        if self._listener is not None:
            self._listener.cancel()
        logger.info(f"Disconnected from Redis.")

    async def subscribe(self, channel: str):
        await self._pubsub.subscribe(channel)
        self._subscribed_channels.add(channel)
        self._ready.set()

    async def psubscribe(self, channel_pattern: str):
        await self._pubsub.psubscribe(channel_pattern)
        self._subscribed_patterns.add(channel_pattern)
        self._ready.set()

    async def unsubscribe(self, channel: str):
        await self._pubsub.unsubscribe(channel)
        self._subscribed_channels.discard(channel)
        if not self._subscribed_channels and not self._subscribed_patterns:
            self._ready.clear()

    async def punsubscribe(self, channel_pattern):
        await self._pubsub.punsubscribe(channel_pattern)
        self._subscribed_patterns.discard(channel_pattern)
        if not self._subscribed_channels and not self._subscribed_patterns:
            self._ready.clear()

    async def publish(self, channel: str, message: Any) -> None:
        await self.conn.publish(channel, message)

    async def next_published(self) -> Event:
        return await self._queue.get()

    async def _pubsub_listener(self) -> None:
        # We does not listen to the pubsub connection if there are no channels subscribed
        # so we need to wait until the first channel is subscribed to start listening
        while True:
            await self._ready.wait()
            # check `listen`'s source code: it stops yielding message when there is
            # no subscribe channels
            async for message in self._pubsub.listen():
                if message["type"] in ("message", "pmessage", ):
                    channel = message["channel"].decode()
                    data = message["data"].decode()
                    pattern = message["pattern"]
                    if pattern is not None: # pmessage
                        # Don't handle same message twice
                        if channel in self._subscribed_channels:
                            continue
                        
                    event = Event(
                        channel=channel,
                        data=data,
                    )
                    await self._queue.put(event)

            self._ready.clear()
        


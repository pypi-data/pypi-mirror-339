import asyncio
import fnmatch # Import for pattern matching
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Set

from loguru import logger

from .lib import Event
from .backends import (
    InMemoryPubSubBackend,
    PubSubBackendInterface,
    RedisPubSubBackend,
    BackendNotSuppoortPatternMatching
)

# --- Exceptions ---

class ClientNotFound(Exception):
    """Raised when an operation is attempted on a non-existent client."""
    pass

class ChannelOrPatternNotFound(Exception):
    """Raised when a client tries to unsubscribe from a channel/pattern it's not in,
       or the channel/pattern doesn't exist in the manager's state."""
    pass

class ConnectionObjectNotProvided(Exception):
    pass

# --- Main Manager Class ---

class GeneralPurposePubSubManager(ABC):
    """
    Manages client subscriptions to channels (exact and patterns) and message
    broadcasting using a PubSub backend.

    Handles client connections, subscriptions, and message dispatching.
    Designed to work with backends providing a single message queue.
    """

    def __init__(
        self,
        url: Optional[str] = None,
        backend: Optional[PubSubBackendInterface] = None,
        batch_size: int = 10, # TODO: Implement batching
        batch_interval: float = 0.1,  # TODO: Implement batching (10 fps)
        rate_limit: Optional[int] = None, # TODO: Implement rate limiting
        rate_period: float = 60.0, # TODO: Implement rate limiting
        unsubscribe_on_empty: bool = True # Applies to both channels and patterns
    ):
        """
        Initializes the PubSub Manager.

        Args:
            url: Connection URL for the backend (e.g., "memory://", "redis://...").
                 Ignored if `backend` is provided.
            backend: An instance of PubSubBackendInterface. If provided, `url` is ignored.
            unsubscribe_on_empty: If True, the manager will automatically call
                `unsubscribe`/`punsubscribe` on the backend when the last local client
                leaves an exact channel or a pattern subscription.


        NOTE Please read the your-chosen backend's document string before using it
        """
        if backend:
            self.psb = backend
            logger.info(f"Using provided backend: {type(backend).__name__}")
        elif url is None or url.startswith("memory://"):
            self.psb = InMemoryPubSubBackend(url)
            logger.info("Using In-Memory PubSub Backend")
        elif url.startswith("redis://"):
            self.psb = RedisPubSubBackend(url)
            logger.info(f"Using Redis PubSub Backend with URL: {url}")
        else:
            raise ValueError(f"Unsupported URL scheme or no backend provided: {url}")

        self.unsubscribe_on_empty = unsubscribe_on_empty
        self._dict_ops_lock = asyncio.Lock()

        # --- State Management ---
        # Maps client_id -> connection object (e.g., WebSocket connection)
        self.client_connection: Dict[str, Any] = {}

        # Exact Channel Subscriptions
        # Maps client_id -> set of exact channels subscribed to
        self.client_exact_channels: Dict[str, Set[str]] = {}
        # Maps exact channel -> set of client_ids subscribed
        self.exact_channel_clients: Dict[str, Set[str]] = {}

        # Pattern Channel Subscriptions
        # Maps client_id -> set of patterns subscribed to
        self.client_pattern_channels: Dict[str, Set[str]] = {}
        # Maps pattern -> set of client_ids subscribed
        self.pattern_channel_clients: Dict[str, Set[str]] = {}


        # --- Central Listener ---
        self._central_listener_task: asyncio.Task | None = None
        self._stop_event = asyncio.Event() # Used to signal listener shutdown

        # --- Batching & Rate Limiting (Placeholders) ---
        self.batch_size = batch_size
        self.batch_interval = batch_interval
        self.message_batches: Dict[str, List[Any]] = {}
        self.batch_tasks: Dict[str, asyncio.Task] = {}

        self.rate_limit = rate_limit
        self.rate_period = rate_period
        self.client_message_counts: Dict[str, List[float]] = {}

    async def initialize(self):
        """Initialize the connection to the PubSub backend and start the listener."""
        logger.info("Initializing PubSub Manager...")
        await self.psb.connect()
        self._stop_event.clear()
        self._central_listener_task = asyncio.create_task(self._run_central_listener())
        logger.info("PubSub Manager initialized and listener started.")

    async def cleanup(self):
        """Clean up resources: stop the listener and disconnect the backend."""
        logger.info("Cleaning up PubSub Manager...")
        # Stop the listener task
        if self._central_listener_task and not self._central_listener_task.done():
            self._stop_event.set() # Signal the listener to stop
            try:
                # Give it a moment to shut down gracefully
                await asyncio.wait_for(self._central_listener_task, timeout=2.0)
            except asyncio.TimeoutError:
                logger.warning("Central listener task did not shut down gracefully, cancelling.")
                self._central_listener_task.cancel()
                try:
                    await self._central_listener_task # Await cancellation
                except asyncio.CancelledError:
                    logger.info("Central listener task cancelled.")
            except Exception as e:
                logger.error(f"Error during central listener shutdown: {e}")

        # Disconnect from the backend
        await self.psb.disconnect()
        logger.info("PubSub Manager cleaned up.")

    async def _run_central_listener(self):
        """Listens for messages from the backend queue and dispatches them."""
        logger.info("Central listener started.")
        try:
            while not self._stop_event.is_set():
                try:
                    # Wait for the next message from the backend's queue
                    event: Optional[Event] = await asyncio.wait_for(self.psb.next_published(), timeout=0.5)
                    logger.debug(f"Received event via central listener: Ch={event.channel}, Data={event.data}")

                    # Dispatch the message data to subscribed clients (handles patterns)
                    # Note: event.channel here is the *concrete* channel the message arrived on.
                    await self.dispatch_message(event.channel, event.data)

                except asyncio.TimeoutError:
                    # No message received, loop continues to check stop_event
                    continue
                except asyncio.CancelledError:
                    logger.info("Central listener task cancellation requested.")
                    break
                except Exception as e:
                    # Log specifics, especially if it's related to message processing
                    logger.exception(f"Error in central listener loop: {e}")
                    # Add a small delay to prevent rapid error loops
                    await asyncio.sleep(1)

        except asyncio.CancelledError:
            logger.info("Central listener task finally cancelled.")
        finally:
            logger.info("Central listener stopped.")

            
    @abstractmethod
    async def send_to_client(self, client_id: str, message: str):
        """
        Abstract method to send a message to a specific client's connection.
        Subclasses must implement this based on their connection object type.
        """
        pass

    async def _get_client_ids_subscribed_to_channel(self, concrete_channel: str) -> Set[str]:
        """
        Finds client IDs subscribed exactly or via pattern, minimizing lock duration.
        """
        exact_subscribers_copy: Set[str] = set()
        patterns_clients_copy: Dict[str, Set[str]] = {}

        async with self._dict_ops_lock:
            exact_subscribers_copy = self.exact_channel_clients.get(concrete_channel, set()).copy()
            if self.pattern_channel_clients:
                 patterns_clients_copy = self.pattern_channel_clients.copy()
                 
        recipient_client_ids: Set[str] = exact_subscribers_copy # Start with the copied exact matches

        # TODO improve performance more
        # like use lru cache, use Tire data structure for simple prefix/suffix patterns
        # (e.g. `pre:*`)
        for pattern, client_set in patterns_clients_copy.items():
            if fnmatch.fnmatch(concrete_channel, pattern):
                recipient_client_ids.update(client_set)

        return recipient_client_ids


    async def dispatch_message(self, concrete_channel: str, message: str):
        """
        Finds all clients subscribed (exactly or via pattern) to the
        concrete_channel and sends them the message.
        """

        recipient_client_ids = list(await self._get_client_ids_subscribed_to_channel(concrete_channel))

        if not recipient_client_ids:
            return

        # logger.debug(f"Dispatching message on '{concrete_channel}' to clients: {recipient_client_ids}")

        send_tasks = []
        for client_id in recipient_client_ids:
            # client is possible disconnected in this short time period
            if client_id in self.client_connection:
                 send_tasks.append(self.send_to_client(client_id, message))


        if send_tasks:
            results = await asyncio.gather(*send_tasks, return_exceptions=True)
            for i, result in enumerate(results):
                 if isinstance(result, Exception):
                      failed_client_id = recipient_client_ids[i]
                      logger.error(f"Error sending message to client {failed_client_id} for channel {concrete_channel}: {result}")


    async def publish(self, channel: str, message: str):
        """Publishes a message to a specific channel via the backend."""
        await self.psb.publish(channel, message)

    async def subscribe(
        self,
        client_id: str,
        channel_or_pattern: str,
        conn: Any = None,
        pattern_matching: bool = False,
    ):
        """
        Subscribes a client connection to a specific channel or pattern.

        If it's the first time connecting this client_id, `conn` must be provided.
        """
        if pattern_matching and not self.psb.support_pattern_matching:
            raise BackendNotSuppoortPatternMatching()

        should_subscribe_backend = False
        async with self._dict_ops_lock:
            # --- Handle Connection ---
            if client_id not in self.client_connection:
                if conn is None:
                    raise ConnectionObjectNotProvided(
                        f"Connection object not provided for new client {client_id}"
                    )
                logger.debug(f"Accepting new connection for client {client_id}")
                self.client_connection[client_id] = conn
            elif conn is not None:
                 # Optionally update connection object if provided for existing client
                 self.client_connection[client_id] = conn

            # --- Handle Subscription Type ---
            if pattern_matching:
                logger.debug(f"Client {client_id} subscribing to pattern: {channel_or_pattern}")
                client_subs = self.client_pattern_channels.setdefault(client_id, set())
                client_subs.add(channel_or_pattern)

                pattern_subs = self.pattern_channel_clients.setdefault(channel_or_pattern, set())
                if not pattern_subs: # First client for this pattern locally
                    should_subscribe_backend = True
                pattern_subs.add(client_id)

            else: # Exact channel subscription
                logger.debug(f"Client {client_id} subscribing to exact channel: {channel_or_pattern}")
                client_subs = self.client_exact_channels.setdefault(client_id, set())
                client_subs.add(channel_or_pattern)

                channel_subs = self.exact_channel_clients.setdefault(channel_or_pattern, set())
                if not channel_subs:
                    should_subscribe_backend = True
                channel_subs.add(client_id)

        # --- Interact with Backend ---
        if should_subscribe_backend:
            if pattern_matching:
                await self.psb.psubscribe(channel_or_pattern)
                logger.info(f"Backend psubscribed to pattern: {channel_or_pattern}")
            else:
                await self.psb.subscribe(channel_or_pattern)
                logger.info(f"Backend subscribed to channel: {channel_or_pattern}")


    async def unsubscribe(
        self,
        client_id: str,
        channel_or_pattern: str,
        pattern_matching: bool = False # Important to know which type to unsubscribe
    ):
        """
        Unsubscribes a client from a specific channel or pattern.
        """
        if pattern_matching and not self.psb.support_pattern_matching:
            raise BackendNotSuppoortPatternMatching()
        
        if client_id not in self.client_connection:
            # Allow unsubscribing even if connection object is gone
            logger.warning(f"Client {client_id} not found in connections, proceeding with state cleanup for unsubscribe.")

        should_unsubscribe_backend = False
        async with self._dict_ops_lock:
            if pattern_matching:
                logger.debug(f"Client {client_id} unsubscribing from pattern: {channel_or_pattern}")
                client_pattern_subs = self.client_pattern_channels.get(client_id)
                if client_pattern_subs:
                    client_pattern_subs.discard(channel_or_pattern)
                    if not client_pattern_subs:
                        del self.client_pattern_channels[client_id]
                else:
                    logger.warning(f"Client {client_id} has no recorded pattern subscriptions.")

                pattern_subs = self.pattern_channel_clients.get(channel_or_pattern)
                if pattern_subs:
                    pattern_subs.discard(client_id)
                    if not pattern_subs: # Last client for this pattern
                        del self.pattern_channel_clients[channel_or_pattern]
                        if self.unsubscribe_on_empty:
                            should_unsubscribe_backend = True
                else:
                    # This implies inconsistency if client thought it was subscribed
                    logger.warning(f"Pattern {channel_or_pattern} not found in pattern_clients during unsubscribe for {client_id}")
                    # raise ChannelOrPatternNotFound(f"Pattern {channel_or_pattern} is not found.") # Or log

            else: # Exact channel unsubscription
                logger.debug(f"Client {client_id} unsubscribing from exact channel: {channel_or_pattern}")
                client_exact_subs = self.client_exact_channels.get(client_id)
                if client_exact_subs:
                    client_exact_subs.discard(channel_or_pattern)
                    if not client_exact_subs: # Remove client entry if no channels left
                        del self.client_exact_channels[client_id]
                else:
                     logger.warning(f"Client {client_id} has no recorded exact channel subscriptions.")

                channel_subs = self.exact_channel_clients.get(channel_or_pattern)
                if channel_subs:
                    channel_subs.discard(client_id)
                    if not channel_subs:
                        del self.exact_channel_clients[channel_or_pattern]
                        if self.unsubscribe_on_empty:
                             should_unsubscribe_backend = True
                else:
                    logger.warning(f"Channel {channel_or_pattern} not found in exact_channel_clients during unsubscribe for {client_id}")
                    # raise ChannelOrPatternNotFound(f"Channel {channel_or_pattern} is not found.") # Or log


        # --- Interact with Backend (outside lock) ---
        if should_unsubscribe_backend:
            if pattern_matching:
                await self.psb.punsubscribe(channel_or_pattern)
                logger.info(f"Backend punsubscribed from pattern: {channel_or_pattern} (last local subscriber left)")
            else:
                await self.psb.unsubscribe(channel_or_pattern)
                logger.info(f"Backend unsubscribed from channel: {channel_or_pattern} (last local subscriber left)")


    async def disconnect(self, client_id: str):
        """Disconnects a client entirely, unsubscribing from all channels and patterns."""
        if client_id not in self.client_connection:
            # Log warning but proceed to clean up state in case it's orphaned
            logger.warning(f"Attempting to disconnect client {client_id} not found in active connections. Cleaning up state...")
            # raise ClientNotFound(f"Client {client_id} not found.") # Or allow cleanup?

        logger.debug(f"Disconnecting client {client_id}...")

        exact_channels_to_unsubscribe_backend = []
        pattern_channels_to_unsubscribe_backend = []

        async with self._dict_ops_lock:
            # Remove the connection object (if it exists)
            self.client_connection.pop(client_id, None)

            # --- Clean up exact channel subscriptions ---
            exact_channels_left = self.client_exact_channels.pop(client_id, set())
            for channel in exact_channels_left:
                if channel in self.exact_channel_clients:
                    self.exact_channel_clients[channel].discard(client_id)
                    if not self.exact_channel_clients[channel]: # Channel is now empty
                        del self.exact_channel_clients[channel]
                        if self.unsubscribe_on_empty:
                            exact_channels_to_unsubscribe_backend.append(channel)

            # --- Clean up pattern subscriptions ---
            patterns_left = self.client_pattern_channels.pop(client_id, set())
            for pattern in patterns_left:
                if pattern in self.pattern_channel_clients:
                    self.pattern_channel_clients[pattern].discard(client_id)
                    if not self.pattern_channel_clients[pattern]: # Pattern is now empty
                        del self.pattern_channel_clients[pattern]
                        if self.unsubscribe_on_empty:
                            pattern_channels_to_unsubscribe_backend.append(pattern)

            # logger.debug(f"Client {client_id} removed. "
            #              f"Exact channels left: {exact_channels_left}. "
            #              f"Patterns left: {patterns_left}. "
            #              f"Empty exact channels for backend unsubscribe: {channels_to_unsubscribe_backend}. "
            #              f"Empty patterns for backend unsubscribe: {patterns_to_unsubscribe_backend}")

        # --- Unsubscribe backend for channels/patterns that are now empty ---
        unsubscribe_tasks = []
        if exact_channels_to_unsubscribe_backend:
            unsubscribe_tasks.extend(self.psb.unsubscribe(ch) for ch in exact_channels_to_unsubscribe_backend)

        if pattern_channels_to_unsubscribe_backend:
            unsubscribe_tasks.extend(self.psb.punsubscribe(p) for p in pattern_channels_to_unsubscribe_backend)

        all_channels = exact_channels_to_unsubscribe_backend + pattern_channels_to_unsubscribe_backend

        if unsubscribe_tasks:
            results = await asyncio.gather(*unsubscribe_tasks, return_exceptions=True)
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    # Determine if it was a channel or pattern based on the original lists
                    # This is approximate if both lists were non-empty
                    item = all_channels[i]
                    is_pattern = i >= len(exact_channels_to_unsubscribe_backend)
                    logger.error(f"Failed backend unsubscribe for {'pattern' if is_pattern else 'channel'} '{item}' during disconnect of {client_id}: {result}")

        logger.info(f"Client {client_id} disconnected successfully.")


# --- Example Implementation ---

# If you want to have more customized experience in handling messages,
# please override `dispatch_message` method

class DumbBroadcaster(GeneralPurposePubSubManager):
    """
    Example broadcaster where the connection object passed in `subscribe`
    must have an asynchronous `send(str)` method.
    """
    def __init__(self, url: str, **kwargs):
        super().__init__(url, **kwargs)

    async def send_to_client(self, client_id: str, message: str):
        """Sends the message using the stored connection object's send method."""
        conn = self.client_connection.get(client_id)
        if conn:
            try:
                await conn.send(message)
            except Exception as e:
                logger.error(f"Failed to send message to client {client_id}: {e}")
        else:
            logger.warning(f"Attempted to send message to client {client_id}, but connection object was missing.")

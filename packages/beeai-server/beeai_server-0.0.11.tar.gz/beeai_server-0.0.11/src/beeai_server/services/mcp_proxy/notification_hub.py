# Copyright 2025 IBM Corp.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import asyncio
import logging
from asyncio import CancelledError
from collections import defaultdict
from contextlib import AsyncExitStack, asynccontextmanager, suppress
from typing import Callable, TYPE_CHECKING, Any

import anyio
from anyio import CancelScope
from anyio.abc import TaskGroup
from anyio.streams.memory import MemoryObjectReceiveStream, MemoryObjectSendStream
from acp.types import AgentRunProgressNotification

from beeai_server.services.mcp_proxy.constants import NotificationStreamType
from acp import ServerNotification, ServerSession, ProgressNotification
from acp.shared.context import RequestContext

if TYPE_CHECKING:
    # Prevent circular import
    from beeai_server.services.mcp_proxy.provider import LoadedProvider

logger = logging.getLogger(__name__)


class NotificationHub:
    """
    Manage notifications from multiple providers using observer pattern:
      - aggregate notifications from all providers into a single stream
      - broadcast notifications to subscribers
      - send request-specific notifications to subscribers
    """

    _notification_stream_reader: MemoryObjectReceiveStream[ServerNotification]
    _notification_stream_writer: MemoryObjectSendStream[ServerNotification]
    _notification_pipe: TaskGroup

    def __init__(self):
        self._exit_stack = AsyncExitStack()
        self._notification_subscribers: set[Callable[[ServerNotification], None]] = set()
        self._notification_stream_writer, self._notification_stream_reader = anyio.create_memory_object_stream[
            ServerNotification
        ]()
        self._provider_cleanups: dict[str, Callable[[], Any]] = defaultdict(lambda: lambda: None)

    async def register(self, loaded_provider: "LoadedProvider"):
        self._notification_pipe.start_soon(self._subscribe_for_messages, loaded_provider)
        logger.info(f"Started listening for notifications from: {loaded_provider.id}")

    async def remove(self, loaded_provider: "LoadedProvider"):
        if loaded_provider.id in self._provider_cleanups:
            self._provider_cleanups[loaded_provider.id]()
            logger.info("Stopped listening for notifications")

    @asynccontextmanager
    async def forward_notifications(
        self,
        session: ServerSession,
        streams=NotificationStreamType.BROADCAST,
        request_context: RequestContext | None = None,
    ):
        if streams == NotificationStreamType.PROGRESS and not request_context:
            raise ValueError(f"Missing request context for {NotificationStreamType.PROGRESS} notifications")

        tasks = []

        def forward_notification(notification: ServerNotification):
            event_loop = asyncio.get_event_loop()
            try:
                match streams:
                    case NotificationStreamType.PROGRESS:
                        if not isinstance(notification, (ProgressNotification, AgentRunProgressNotification)):
                            return
                        if not (request_context.meta and request_context.meta.progressToken):
                            logger.warning("Could not dispatch progress notification, missing progress Token")
                            return
                        if notification.params.progressToken != request_context.meta.progressToken:
                            return
                        notification.model_extra.pop("jsonrpc", None)
                        tasks.append(event_loop.create_task(session.send_notification(notification)))
                    case NotificationStreamType.BROADCAST:
                        if isinstance(notification, (ProgressNotification, AgentRunProgressNotification)):
                            return
                        notification.model_extra.pop("jsonrpc", None)
                        tasks.append(event_loop.create_task(session.send_notification(notification)))
            except anyio.BrokenResourceError:
                # TODO why the resource broken - need proper cleanup?
                self._notification_subscribers.remove(forward_notification)

        try:
            self._notification_subscribers.add(forward_notification)
            yield
        finally:
            try:
                await asyncio.gather(*tasks)
            except Exception as ex:
                logger.warning(f"Exception occured when sending notifications: {ex}")
            self._notification_subscribers.remove(forward_notification)

    async def _forward_notifications_loop(self):
        async for message in self._notification_stream_reader:
            for forward_message_handler in self._notification_subscribers.copy():
                try:
                    forward_message_handler(message)
                except Exception as e:
                    logger.warning(f"Failed to forward notification: {e}", exc_info=e)

    async def _subscribe_for_messages(self, loaded_provider: "LoadedProvider"):
        async def subscribe():
            with CancelScope():
                try:
                    async for message in loaded_provider.incoming_messages:
                        match message:
                            case ServerNotification(root=notify):
                                logger.debug(f"Dispatching notification {notify.method}")
                                await self._notification_stream_writer.send(notify)
                except CancelledError:
                    logger.info("Reading messages cancelled.")
                except (anyio.BrokenResourceError, anyio.EndOfStream) as ex:
                    logger.error(f"Exception occured during reading messages: {ex!r}")

        task = asyncio.create_task(subscribe())
        self._provider_cleanups[loaded_provider.id] = task.cancel
        with suppress(CancelledError):
            await task

    async def __aenter__(self):
        self._notification_pipe = await self._exit_stack.enter_async_context(anyio.create_task_group())
        await self._exit_stack.enter_async_context(self._notification_stream_writer)
        await self._exit_stack.enter_async_context(self._notification_stream_reader)
        self._notification_pipe.start_soon(self._forward_notifications_loop)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._exit_stack.aclose()

import asyncio
from typing import Awaitable
from typing import Callable
from typing import Generic
from typing import Iterable
from typing import List
from typing import TypeVar

from imbue_core.async_monkey_patches import log_exception
from imbue_core.async_monkey_patches import safe_cancel_and_wait_for_cleanup
from imbue_core.clean_tasks import create_clean_task

_EVENT_TYPE = TypeVar("_EVENT_TYPE")  # Generic type for logged objects


class BackgroundBatchLogger(Generic[_EVENT_TYPE]):
    """A generic background logger that accumulates and asynchronously flushes logs in batches in the background.

    Partly Written by ChatGPT: https://chatgpt.com/share/67f4512f-97ac-800a-b763-442a5a13c346
    """

    def __init__(
        self,
        write_to_storage: Callable[[List[_EVENT_TYPE]], Awaitable[None]],
        name: str,
        flush_interval_seconds: float,
    ) -> None:
        self.queue: asyncio.Queue[_EVENT_TYPE] = asyncio.Queue()
        self.name: str = name
        self.flush_interval: float = flush_interval_seconds
        self._shutdown_event: asyncio.Event = asyncio.Event()
        self._write_to_storage: Callable[[List[_EVENT_TYPE]], Awaitable[None]] = write_to_storage
        self._task: asyncio.Task[None] = create_clean_task(
            self._background_worker(), name=name, is_within_new_group=True
        )

    def log(self, obj: Iterable[_EVENT_TYPE]) -> None:
        """Enqueue an object to be logged."""
        if self._shutdown_event.is_set():
            raise RuntimeError("Logger is shutting down, cannot accept new logs")
        for item in obj:
            # Queue does not have a max size, so this will never actually block.
            self.queue.put_nowait(item)

    async def flush(self) -> None:
        """Flush all queued logs."""
        batch: List[_EVENT_TYPE] = []
        while not self.queue.empty():
            batch.append(await self.queue.get())
        if batch:
            try:
                await self._write_to_storage(batch)
            except Exception as e:
                log_exception(
                    e,
                    f"Error writing batch to storage for logger {self.name}.  We're going to otherwise ignore this error.",
                )

    async def shutdown(self) -> None:
        """Gracefully shut down and flush remaining logs."""
        self._shutdown_event.set()
        await self.flush()
        await safe_cancel_and_wait_for_cleanup(self._task)

    async def _background_worker(self) -> None:
        """Background task that accumulates and flushes logs in batches."""
        while not self._shutdown_event.is_set():
            try:
                await asyncio.sleep(self.flush_interval)  # Debounce time
                await self.flush()
            except asyncio.CancelledError:
                break

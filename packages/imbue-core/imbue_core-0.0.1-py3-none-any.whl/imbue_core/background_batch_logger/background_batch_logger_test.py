import asyncio
import inspect
from typing import List
from typing import Optional

import attr
import pytest

from imbue_core.background_batch_logger.background_batch_logger import BackgroundBatchLogger


def _get_current_test_name() -> str:
    """Helper function to get the name of the current test function."""

    frame = inspect.currentframe()
    if frame is None:
        # Fallback if frame inspection is not available
        return "unknown_test"
    # Go up two frames: one for this function, one for the test function
    caller_frame = frame.f_back
    if caller_frame is None:
        return "unknown_test"
    caller_frame = caller_frame.f_back
    if caller_frame is None:
        return "unknown_test"
    return caller_frame.f_code.co_name


@attr.s(auto_attribs=True)
class _StrAccumulator:
    """Used to test that batches came in as expected."""

    batches: List[List[str]] = attr.ib(default=attr.Factory(list))

    async def process_batch(self, batch: List[str]) -> None:
        self.batches.append(batch)


async def test_no_events_are_logged() -> None:
    """Test that no events are lost when logging in batches."""
    accumulator = _StrAccumulator()
    logger = BackgroundBatchLogger[str](
        accumulator.process_batch, flush_interval_seconds=1.0, name=_get_current_test_name()
    )
    assert logger.queue.empty()
    await logger.shutdown()
    assert accumulator.batches == []


async def test_log_two_batches() -> None:
    """Test that no events are lost when logging in batches."""
    accumulator = _StrAccumulator()
    # if this test is flaky, try increasing the flush interval.
    # I couldn't think of a better way to test that the flushes are indeed happening using the clock.
    logger = BackgroundBatchLogger[str](
        accumulator.process_batch, flush_interval_seconds=0.25, name=_get_current_test_name()
    )
    logger.log(["hello", "there"])
    logger.log(["beautiful"])
    assert accumulator.batches == []
    await asyncio.sleep(logger.flush_interval * 2.0)
    assert accumulator.batches == [["hello", "there", "beautiful"]]

    logger.log(["world"])
    await logger.shutdown()
    assert accumulator.batches == [["hello", "there", "beautiful"], ["world"]]


async def test_log_shutdown_with_very_long_flush_interval() -> None:
    """Test that no events are lost when logging in batches."""
    accumulator = _StrAccumulator()
    logger = BackgroundBatchLogger[str](
        accumulator.process_batch, flush_interval_seconds=1e6, name=_get_current_test_name()
    )
    logger.log(["hello", "there"])
    logger.log(["beautiful"])
    logger.log(["world"])
    assert accumulator.batches == []
    await logger.shutdown()
    assert accumulator.batches == [["hello", "there", "beautiful", "world"]]


async def test_log_after_shutdown_fails() -> None:
    """Test that logging after shutdown fails."""
    accumulator = _StrAccumulator()
    logger = BackgroundBatchLogger[str](
        accumulator.process_batch, flush_interval_seconds=1.0, name=_get_current_test_name()
    )
    await logger.shutdown()
    with pytest.raises(RuntimeError):
        logger.log(["hello"])


async def _raise_exception(batch: List[str]) -> None:
    raise ValueError("test exception")


async def test_callback_raises_exception() -> None:
    """Test that a callback that raises an exception does not crash the logger."""
    accumulator = _StrAccumulator()
    logger = BackgroundBatchLogger[str](_raise_exception, flush_interval_seconds=1.0, name=_get_current_test_name())
    logger.log(["hello"])
    await logger.shutdown()
    # Exception happens here, but is swallowed other than logging it.
    # TODO(thad): Consider adding another callback for exceptions invoking the callback?
    assert accumulator.batches == []


@attr.s(auto_attribs=True)
class _StrAccumulatorWithSemaphore:
    semaphore: Optional[asyncio.Semaphore] = None
    batches: List[List[str]] = attr.ib(default=attr.Factory(list))

    async def process_batch(self, batch: List[str]) -> None:
        if self.semaphore is not None:
            await self.semaphore.acquire()
        self.batches.append(batch)


async def test_callback_blocks_a_bit() -> None:
    accumulator = _StrAccumulatorWithSemaphore()
    # Create a semaphore with 0 permits, which means it will block until released
    accumulator.semaphore = asyncio.Semaphore(0)
    logger = BackgroundBatchLogger[str](
        accumulator.process_batch, flush_interval_seconds=1e6, name=_get_current_test_name()
    )
    logger.log(["hello"])
    # Foreground flush would block because the callback is blocking.
    background_flush_task = asyncio.create_task(logger.flush(), name="test_callback_blocks_a_bit background flush")
    await asyncio.sleep(0.01)
    # Even after waiting, the logger is still blocked.
    assert accumulator.batches == []
    # Unblock the logger.
    accumulator.semaphore.release()
    await background_flush_task
    assert accumulator.batches == [["hello"]]

    # Create a new semaphore for the next test
    accumulator.semaphore = asyncio.Semaphore(0)
    logger.log(["world"])

    background_shutdown_task = asyncio.create_task(logger.shutdown(), name="test_callback_blocks_a_bit shutdown")
    await asyncio.sleep(0.01)
    # Even after waiting, the logger callback is still blocking on the semaphore.
    assert accumulator.batches == [["hello"]]
    accumulator.semaphore.release()
    await background_shutdown_task
    assert accumulator.batches == [["hello"], ["world"]]

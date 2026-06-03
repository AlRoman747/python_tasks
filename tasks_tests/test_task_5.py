import asyncio
import pytest

from tasks_solving.task_5 import AsyncBatcher

def test_invalid_size():
    async def source():
        yield 1

    with pytest.raises(ValueError):
        AsyncBatcher(source(), 0)

    with pytest.raises(ValueError):
        AsyncBatcher(source(), -1)

@pytest.mark.asyncio
async def test_empty_source():
    async def source():
        if False:
            yield

    result = [batch async for batch in AsyncBatcher(source(), 3)]

    assert result == []

@pytest.mark.asyncio
async def test_partial_last_batch():
    async def source():
        for i in range(5):
            yield i

    result = [batch async for batch in AsyncBatcher(source(), 3)]

    assert result == [[0, 1, 2],  [3, 4]]

@pytest.mark.asyncio
async def test_size_one():
    async def source():
        for i in range(3):
            yield i

    result = [batch async for batch in AsyncBatcher(source(), 1)]

    assert result == [[0], [1], [2]]

class AsyncIterable:
    def __aiter__(self):
        return self._gen()

    async def _gen(self):
        yield 1
        yield 2


@pytest.mark.asyncio
async def test_async_iterable_supported():
    result = [batch async for batch in AsyncBatcher(AsyncIterable(), 2)]

    assert result == [[1, 2]]


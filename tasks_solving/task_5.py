class AsyncBatcher:
    def __init__(self, source, size: int) -> None:
        if size <= 0:
            raise ValueError(f"size should be > 0")
        self._size: int = size
        self._source = self._to_async_iterator(source)
        self._exhausted: bool = False


    @staticmethod
    def _to_async_iterator(source):
        if hasattr(source, "__anext__"):
            return source
        if hasattr(source, "__aiter__"):
            #итератор
            return source.__aiter__()
        raise TypeError("source should be an async iterator or async iterable" )


    def __aiter__(self) -> "AsyncBatcher":
        return self

    async def __anext__(self) -> list:
        if self._exhausted:
            raise StopAsyncIteration

        batch = []
        for _ in range(self._size):
            try:
                item = await self._source.__anext__()
                batch.append(item)
            except StopAsyncIteration:
                self._exhausted = True
                break
        if not batch:
            raise StopAsyncIteration

        return batch

    async def aclose(self) -> None:
        self._exhausted = True
        if hasattr(self._source, "aclose"):
            await self._source.aclose()

    async def __aenter__(self) -> "AsyncBatcher":
        return self

    async def __aexit__(self, *args) -> None:
        await self.aclose()
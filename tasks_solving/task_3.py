from collections import deque
from typing import Any, Iterator


class RewindableStream:
    def __init__(self, source: Any, capacity: int) -> None:
        if capacity <= 0:
            raise ValueError(f"capacity should be > 0")

        self._source: Iterator[Any] = iter(source)
        self._capacity = capacity
        self._history: deque[Any] = deque(maxlen=capacity)
        self._rewind_debt = 0

    def __iter__(self) -> "RewindableStream":
        """Поток сам является итератором"""
        return self

    def __next__(self) -> Any:
        if self._rewind_debt > 0:
            idx = -self._rewind_debt
            value = self._history[idx]
            self._rewind_debt -= 1
            return value

        value = next(self._source)
        self._history.append(value)
        return value


    def rewind(self, steps: int = 1) -> None:
        if steps <= 0:
            raise ValueError(f"steps must be > 0")

        available = len(self._history) - self._rewind_debt
        if steps > available:
            raise ValueError(f"Cannot rewind {steps}")
        self._rewind_debt += steps
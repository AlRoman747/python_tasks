"""Тесты для RewindableStream."""
import pytest
from tasks_solving.task_3 import RewindableStream


def gen(*values):
    """Вспомогательный генератор."""
    yield from values


class TestRewindableStreamBasic:
    def test_list_source_basic(self):
        stream = RewindableStream([1, 2, 3], capacity=3)
        assert list(stream) == [1, 2, 3]

    def test_generator_source(self):
        stream = RewindableStream(gen(10, 20, 30), capacity=3)
        assert list(stream) == [10, 20, 30]

    def test_empty_source(self):
        stream = RewindableStream([], capacity=5)
        assert list(stream) == []


class TestRewindableStreamCapacity:
    def test_rewind_beyond_capacity_raises(self):
        """Нельзя откатиться дальше capacity."""
        stream = RewindableStream([1, 2, 3, 4, 5], capacity=2)
        next(stream)   # 1
        next(stream)   # 2
        next(stream)   # 3 — теперь в истории только [2, 3]
        with pytest.raises(ValueError):
            stream.rewind(3)   # больше, чем capacity

    def test_history_eviction(self):
        stream = RewindableStream(range(10), capacity=3)
        for _ in range(7):
            next(stream)
        stream.rewind(3)   # откат на 3 доступных шага назад
        assert next(stream) == 4
        assert next(stream) == 5
        assert next(stream) == 6

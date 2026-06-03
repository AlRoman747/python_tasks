import pytest
from tasks_solving.task_2 import cached_method


class Counter:

    def __init__(self, value: int) -> None:
        self._value = value
        self.calls: int = 0

    @cached_method
    def total(self) -> int:
        self.calls += 1
        return self._value * 2

    @cached_method
    def data(self) -> list[int]:
        """Метод, возвращающий изменяемый объект."""
        self.calls += 1
        return [1, 2, 3]


def test_result_correct():
    c = Counter(5)
    assert c.total() == 10

def test_cached_second_call():
    """Повторный вызов не должен перевычислять результат"""
    c = Counter(5)
    c.total()
    c.total()
    assert c.calls == 1

def test_called_many_times():
    c = Counter(7)
    for _ in range(10):
        c.total()
    assert c.calls == 1


def test_two_instances_independent():
    """Два экземпляра класса имеют независимый кэш"""
    c1 = Counter(1)
    c2 = Counter(2)
    assert c1.total() == 2
    assert c2.total() == 4
    assert c1.calls == 1
    assert c2.calls == 1

def test_no_state_mixing():
    """Изменение кэша одного экземпляра не влияет на другой"""
    c1 = Counter(10)
    c2 = Counter(10)
    r1 = c1.total()
    Counter.total.clear(c1)
    c1.total()
    c2.total()
    assert c1.calls == 2   # вычислил дважды
    assert c2.calls == 1   # вычислил один раз

def test_multiple_cached_methods_independent():
    c = Counter(3)
    c.total()
    c.data()
    assert c.calls == 2   # каждый метод вызван один раз
    c.total()
    c.data()
    assert c.calls == 2   # из кэша


def test_class_access_returns_descriptor():
    """Доступ через класс возвращает дескриптор, а не вызывает метод"""
    descriptor = Counter.total
    assert isinstance(descriptor, cached_method)



def test_clear_cache_forces_recompute():
    c = Counter(5)
    c.total()
    assert c.calls == 1
    Counter.total.clear(c)
    c.total()
    assert c.calls == 2


def test_mutable_result_cached():
    c = Counter(0)
    r1 = c.data()
    r2 = c.data()
    assert r1 is r2   # один и тот же объект из кэша

def test_mutable_result_modification():
    c = Counter(0)
    r1 = c.data()
    r1.append(99)
    r2 = c.data()
    assert 99 in r2   # кэш хранит тот же объект

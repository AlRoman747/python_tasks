import pytest
from tasks_solving.task_1 import AttributeRouter


class Config:
    host: str = "localhost"
    port: int = 8080


class State:
    status: str = "running"
    host: str = "state-host"   # конфликт с Config.host


class BrokenComponent:
    def __getattr__(self, name: str) -> object:
        raise AttributeError(f"BrokenComponent refuses '{name}'")



def test_single_component_attribute() -> None:
        cfg = Config()
        router = AttributeRouter(cfg)
        assert router.host == "localhost"
        assert router.port == 8080

def test_multiple_components_no_conflict() -> None:
        cfg = Config()
        state = State()
        router = AttributeRouter(cfg, state)
        assert router.status == "running"

def test_conflict_first_component_wins() -> None:
        cfg = Config()
        state = State()
        router = AttributeRouter(cfg, state)
        assert router.host == "localhost"

def test_conflict_order_reversed() -> None:
        state = State()
        cfg = Config()
        router = AttributeRouter(state, cfg)
        assert router.host == "state-host"


def test_broken_component_skipped() -> None:
        broken = BrokenComponent()
        cfg = Config()
        router = AttributeRouter(broken, cfg)
        assert router.host == "localhost"

def test_broken_component_only_raises() -> None:
        broken = BrokenComponent()
        router = AttributeRouter(broken)
        with pytest.raises(AttributeError):
            _ = router.something
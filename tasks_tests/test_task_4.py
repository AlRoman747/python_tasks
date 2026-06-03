import pytest
from tasks_solving.task_4 import SafeContextStack

class TrackingCM:
    """Записывает порядок вызовов enter/exit"""

    def __init__(self, name: str, log: list[str], value: object = None):
        self.name = name
        self.log = log
        self._value = value

    def __enter__(self) -> object:
        self.log.append(f"enter:{self.name}")
        return self._value or self.name

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        self.log.append(f"exit:{self.name}")
        return False


class FailingEnterCM(TrackingCM):
    def __enter__(self) -> object:
        self.log.append(f"enter_fail:{self.name}")
        raise RuntimeError(f"Enter failed: {self.name}")


class FailingExitCM(TrackingCM):
    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        self.log.append(f"exit_fail:{self.name}")
        raise RuntimeError(f"Exit failed: {self.name}")


class SuppressingCM(TrackingCM):
    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        self.log.append(f"exit_suppress:{self.name}")
        return True
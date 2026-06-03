import sys


class SafeContextStack:

    def __init__(self, managers):
        self._managers = list(managers)
        # Список уже открытых контекстов пополняется в __enter__
        self._entered = []

    def __exit__(self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb) -> bool:
        return self._cleanup(exc_type, exc_val, exc_tb)

    def _cleanup(self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb) -> bool:
        suppres = False
        pending_exception = None

        for manager in reversed(self._entered):
            try:
                result = manager.__exit__(exc_type, exc_val, exc_tb)
                if result:
                    suppres = True
            except Exception as cleanup_exc:
                if pending_exception is None:
                    pending_exception = cleanup_exc # сохраняется первое исключение из cleanup

        self._entered.clear()

        if pending_exception is not None:
            raise pending_exception

        return suppres

    def __enter__(self):
        results = []
        for manager in self._managers:
            try:
                result = manager.__enter__()
                self._entered.append(manager)
                results.append(result)
            except Exception:
                exc_info = sys.exc_info()
                self._cleanup(None, None, None)
                raise exc_info[1].with_traceback(exc_info[2])

        return results
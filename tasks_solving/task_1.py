class AttributeRouter:
    def __init__(self, *components: object) -> None:
        self._components = components

    def __getattr__(self, name: str) -> object:
        components = object.__getattribute__(self, "_components")

        for component in components:
            try:
                return getattr(component, name)
            except AttributeError:
                continue

        raise AttributeError(name)

    def has_route(self, name: str) -> bool:
        try:
            object.__getattribute__(self, name)
            return True
        except AttributeError:
            pass

        components = object.__getattribute__(self, "_components")
        for component in components:
            try:
                getattr(component, name)
                return True
            except AttributeError:
                pass
        return False
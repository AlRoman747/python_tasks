class cached_method:
    def __init__(self, func):
        self.func = func
        self.cache_name = f"_cached_{func.__name__}"
        self.__name__ = func.__name__

    def __get__(self, instance, owner):
        if instance is None:
            return self

        def wrapper():
            if self.cache_name not in instance.__dict__:
                instance.__dict__[self.cache_name] = self.func(instance)

            return instance.__dict__[self.cache_name]

        wrapper.__name__ = self.func.__name__
        return wrapper

    def clear(self, instance):
        """Сброс кэша"""
        instance.__dict__.pop(self.cache_name, None)

    def __repr__(self) -> str:
        return f"<cached_method {self.func.__qualname__!r}>"
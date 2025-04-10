class BaseKey:
    def __init__(self, key: any = None):
        if type(self) is BaseKey:
            raise TypeError("BaseKey is an abstract class and cannot be instantiated directly.")
        self.key = key

    def __repr__(self):
        return f"{self.__class__.__module__}.{self.__class__.__name__}{f".{self.key}" if self.key is not None else ""}"

    def __hash__(self):
        return hash(self.__repr__())

    def __eq__(self, other):
        if isinstance(other, BaseKey):
            return self.__hash__() == other.__hash__()
        super().__eq__(other)
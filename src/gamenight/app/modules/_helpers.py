from injector import ListOfProviders as _ListOfProviders
from injector import ClassProvider, Provider, Module


# marker class
class GamenightModule(Module):
    pass


class ListOfProviders(_ListOfProviders):

    def __init__(self, classes=()):
        super().__init__()
        for cls in classes:
            self.append(cls)


def _to_class_provider(cls):
    if not isinstance(cls, Provider):
        return ClassProvider(cls)
    return cls


# see alecthomas/injector #45
class ClassProviderList(ListOfProviders):

    def __init__(self, classes=()):
        super().__init__(_to_class_provider(c) for c in classes)

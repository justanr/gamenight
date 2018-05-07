from abc import abstractmethod
from typing import Generic, List, Optional, TypeVar

T = TypeVar('T')


class Repo(Generic[T]):

    @abstractmethod
    def fetch(self, id: int) -> T:
        pass

    @abstractmethod
    def add(self, entity: T) -> None:
        pass

    @abstractmethod
    def remove(self, entity: T) -> None:
        pass

    @classmethod
    def configure(cls):
        pass

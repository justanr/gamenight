from abc import ABC, abstractmethod, abstractproperty
from .game import GameRepo


class UnitOfWorkError(Exception):
    pass


class UnitOfWork(ABC):
    @abstractmethod
    def commit(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def rollback(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def open(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def close(self) -> bool:
        raise NotImplementedError

    def __enter__(self) -> 'UnitOfWork':
        self.open()
        return self

    def __exit__(self, exc_type, value, traceback) -> None:
        self.close()

    @abstractproperty
    def games(self) -> GameRepo:
        raise NotImplementedError


class UnitOfWorkManager(ABC):
    @abstractmethod
    def start(self) -> UnitOfWork:
        raise NotImplementedError

    @classmethod
    def configure(cls) -> None:
        """
        Called once during start up to perform any configuration needed for the
        unit of work. This is an optional hook to implement.
        """
        pass

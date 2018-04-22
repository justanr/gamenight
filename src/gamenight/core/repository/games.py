from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities.game import Game


class GameRepo(ABC):

    @abstractmethod
    def fetch(self, id: int) -> Game:
        pass

    @abstractmethod
    def add(self, game: Game) -> None:
        pass

    @abstractmethod
    def remove(self, game: Game) -> None:
        pass

    @abstractmethod
    def fetch_all(self) -> List[Game]:
        pass

    @abstractmethod
    def by_name(self, name: str) -> Optional[Game]:
        pass

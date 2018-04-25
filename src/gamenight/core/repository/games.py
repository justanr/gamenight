from abc import abstractmethod
from typing import List, Optional

from ..entities.game import Game
from .base import Repo


class GameRepo(Repo[Game]):

    @abstractmethod
    def by_name(self, name: str) -> Optional[Game]:
        pass

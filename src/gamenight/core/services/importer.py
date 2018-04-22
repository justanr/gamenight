from abc import ABC, abstractmethod
from typing import Generic, List, TypeVar

import attr

from ..entities.game import Game

RemoteGameIDType = TypeVar('RemoteGameIDType')


@attr.s
class RemoteGame(Generic[RemoteGameIDType]):
    id: RemoteGameIDType = attr.ib()
    name: str = attr.ib()


class GameImporter(ABC, Generic[RemoteGameIDType]):

    @abstractmethod
    def import_game(self, id: RemoteGameIDType) -> Game:
        pass


class RemoteGameSearch(ABC, Generic[RemoteGameIDType]):

    @abstractmethod
    def search(self, query: str) -> List[RemoteGame[RemoteGameIDType]]:
        pass

    @abstractmethod
    def retrieve(self, id: RemoteGameIDType) -> Game:
        pass

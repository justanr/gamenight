from abc import abstractmethod
from typing import Generic, List, TypeVar
from .remote import RemoteGameIDType

class RemoteGameSearch(Generic[RemoteGameIDType]):

    @abstractmethod
    def search(self, query: str) -> List[RemoteGame[RemoteGameIDType]]:
        pass

    @abstractmethod
    def retrieve(self, id: RemoteGameIDType) -> Game:
        pass

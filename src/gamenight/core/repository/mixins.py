from abc import abstractmethod
from typing import Generic, List, TypeVar

SearchParams = TypeVar("SearchParams")
Entity = TypeVar("Entity")


class Searchable(Generic[Entity, SearchParams]):

    @abstractmethod
    def search(self, params: SearchParams) -> List[Entity]:
        pass

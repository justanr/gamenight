from abc import abstractmethod
from typing import List, Optional

import attr

from ..entities.game import Game
from .base import Repo
from .mixins import Searchable


@attr.s(cmp=False, auto_attribs=True)
class GameSearchParams:
    # game attrs
    name: Optional[str] = attr.ib(default="")
    description: Optional[str] = attr.ib(default="")
    age: Optional[List[int]] = attr.ib(default=attr.Factory(list))
    players: Optional[List[int]] = attr.ib(default=attr.Factory(list))
    tags: Optional[List[str]] = attr.ib(default=attr.Factory(list))

    # pagination controls
    page_size: Optional[int] = attr.ib(default=100)
    last_seen: Optional[int] = attr.ib(default=None)


class GameRepo(Repo[Game], Searchable[Game, GameSearchParams]):

    @abstractmethod
    def by_name(self, name: str) -> Optional[Game]:
        pass

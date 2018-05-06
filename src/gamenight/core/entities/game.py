# -*- coding: utf-8 -*-
"""
    gamenight.core.entities.game
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    :license: MIT, see license for details
    :copyright: 2018 Alec Nikolas Reiter
"""
from typing import List, Optional

import attr


@attr.s(hash=True, cmp=False, auto_attribs=True)
class GameTag:
    name: str = attr.ib()
    id: Optional[int] = attr.ib(default=None)


@attr.s(hash=True, cmp=False, auto_attribs=True)
class Game:
    name: str = attr.ib()
    description: str = attr.ib()
    age: int = attr.ib()
    min_players: int = attr.ib()
    max_players: Optional[int] = attr.ib(default=None)
    tags: List[str] = attr.ib(default=attr.Factory(list), hash=False)
    id: Optional[int] = attr.ib(default=None)


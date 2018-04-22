# -*- coding: utf-8 -*-
"""
    gamenight.core.entities.game
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    :license: MIT, see license for details
    :copyright: 2018 Alec Nikolas Reiter
"""
from typing import List, Optional

import attr


@attr.s
class GameTag:
    name: str = attr.ib()


@attr.s
class Game:
    name: str = attr.ib()
    description: str = attr.ib()
    min_players: int = attr.ib()
    max_players: Optional[int] = attr.ib()
    age: int = attr.ib()
    tags: List[GameTag] = attr.ib()
    id: Optional[int] = attr.ib(default=None)


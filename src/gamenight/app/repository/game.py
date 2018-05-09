from typing import Any, ClassVar, List, Optional

from sqlalchemy import Column, ForeignKey, Integer, String, func
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import mapper

from ...core.entities.game import Game, GameTag
from ...core.repository.game import GameRepo, GameSearchParams
from ..extensions import db


class SQLAGameRepo(GameRepo):
    configured: ClassVar[bool] = False

    def fetch(self, id: int) -> Game:
        game = db.session.query(Game).get(id)
        if game is None:
            raise Exception("Game not found!!!!")
        return game

    def add(self, game: Game) -> None:
        db.session.add(game)

    def remove(self, game: Game) -> None:
        db.session.delete(self.fetch(game.id))

    def by_name(self, name: str) -> Optional[Game]:
        return db.session.query(Game).filter(Game.name == name).first()

    def search(self, params: GameSearchParams) -> List[Game]:
        query = db.session.query(Game)
        query = query.filter(_parse_params_to_query(params))

        if params.page_size is None or params.page_size < 1:
            params.page_size = 100

        else:
            params.page_size = min([params.page_size, 100])

        return query.order_by(Game.id).limit(params.page_size).all()

    @classmethod
    def configure(cls):
        if cls.configured:
            return

        super().configure()
        tags_table = db.Table(
            "tags",
            Column("id", Integer, primary_key=True),
            Column("name", String, unique=True, nullable=False),
        )

        games_table = db.Table(
            "games",
            Column("id", Integer, primary_key=True),
            Column("name", String, unique=True, nullable=False),
            Column("description", String, nullable=False),
            Column("min_players", Integer, nullable=False),
            Column("max_players", Integer, nullable=True),
            Column("age", Integer, nullable=True),
        )

        game_tag_table = db.Table(
            "game_tags",
            Column("id", Integer, primary_key=True),
            Column("game_id", Integer, ForeignKey("games.id"), nullable=False),
            Column("tag_id", Integer, ForeignKey("tags.id"), nullable=False),
        )

        mapper(GameTag, tags_table)
        mapper(
            Game,
            games_table,
            properties={"_tags": db.relationship(GameTag, secondary=game_tag_table)},
        )

        Game.tags = association_proxy("_tags", "name", creator=cls._find_or_create_tag)

        cls.configured = True

    @staticmethod
    def _find_or_create_tag(name):
        tag = db.session.query(GameTag).filter(
            func.lower(GameTag.name) == name.lower()
        ).first()

        if tag is None:
            tag = GameTag(name=name)
            db.session.add(tag)

        return tag


def _parse_params_to_query(params: GameSearchParams) -> Any:
    query_parts: List[Any] = []

    query_parts.extend(_handle_name_param(params.name))
    query_parts.extend(_handle_description_param(params.description))
    query_parts.extend(_handle_age(params.age))
    query_parts.extend(_handle_players(params.players))
    query_parts.extend(_handle_tags(params.tags))
    query_parts.extend(_last_seen(params.last_seen))

    return db.and_(*query_parts)


def _handle_name_param(name: str) -> List[Any]:
    if not name:
        return []
    return [Game.name.ilike(_make_like(name))]  # type: ignore


def _handle_description_param(descript: str) -> List[Any]:
    if not descript:
        return []

    return [Game.description.ilike(_make_like(descript))]  # type: ignore


def _make_like(param: str) -> str:
    if not param.startswith("%"):
        param = f"%{param}"

    if not param.endswith("%"):
        param += "%"

    return param.lower()


def _handle_age(ages: List[int]) -> List[Any]:
    if not ages:
        return []

    how_many = len(ages)

    if how_many == 1:
        return [Game.age >= ages[0]]

    ages.sort()

    return [Game.age >= ages[0], Game.age <= ages[1]]


def _handle_players(players: List[int]) -> List[Any]:
    if not players:
        return []

    if len(players) == 1:
        return [Game.min_players >= players[0]]

    players.sort()

    return [Game.min_players >= players[0], Game.max_players <= players[-1]]


def _handle_tags(tags: List[str]) -> List[Any]:
    if not tags:
        return []

    tags = [t.lower() for t in tags]
    return [Game.tags.any(func.lower(GameTag.name).in_(tags))]  # type: ignore


def _last_seen(id: Optional[int]) -> List[Any]:
    if id is None or id < 1:
        return []

    return [Game.id > id]

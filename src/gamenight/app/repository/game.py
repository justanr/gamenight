from typing import ClassVar, List, Optional

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import mapper

from ...core.entities.game import Game, GameTag
from ...core.repository.games import GameRepo
from ..extensions import db


class SQLAGameRepo(GameRepo):
    configured: ClassVar[bool] = False

    def fetch(self, id: int) -> Game:
        game = db.session.query(Game).get(id)
        if game is None:
            raise Exception('Game not found!!!!')
        return game

    def fetch_all(self) -> List[Game]:
        return db.session.query(Game).order_by(Game.id).all()

    def add(self, game: Game) -> None:
        db.session.add(game)

    def remove(self, game: Game) -> None:
        db.session.delete(self.fetch(game.id))

    def by_name(self, name: str) -> Optional[Game]:
        return db.session.query(Game).filter(Game.name == name).first()

    @classmethod
    def configure(cls):
        if cls.configured:
            return

        super().configure()
        tags_table = db.Table(
            'tags',
            Column('id', Integer, primary_key=True),
            Column('name', String, unique=True, nullable=False)
        )

        games_table = db.Table(
            'games',
            Column('id', Integer, primary_key=True),
            Column('name', String, unique=True, nullable=False),
            Column('description', String, nullable=False),
            Column('min_players', Integer, nullable=False),
            Column('max_players', Integer, nullable=True),
            Column('age', Integer, nullable=True)
        )

        game_tag_table = db.Table(
            'game_tags',
            Column('id', Integer, primary_key=True),
            Column('game_id', Integer, ForeignKey('games.id'), nullable=False),
            Column('tag_id', Integer, ForeignKey('tags.id'), nullable=False)
        )

        mapper(GameTag, tags_table)
        mapper(
            Game,
            games_table,
            properties={
                '_tags': db.relationship(GameTag, secondary=game_tag_table)
            }
        )

        Game.tags = association_proxy(
            '_tags', 'name', creator=cls._find_or_create_tag
        )

        cls.configured = True

    @staticmethod
    def _find_or_create_tag(name):
        tag = db.session.query(GameTag).filter(GameTag.name == name).first()

        if tag is None:
            tag = GameTag(name=name)
            db.session.add(tag)

        return tag

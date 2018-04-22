from typing import List, Optional

from injector import inject
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import Session

from ...core.entities.game import Game as GameEntity
from ...core.entities.game import GameTag as GameTag_
from ...core.repository.games import GameRepo
from ..extensions import db


class Game(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    description = Column(String)
    min_players = Column(Integer)
    max_players = Column(Integer)
    age = Column(Integer)
    gametags = db.relationship('Tag', secondary='game_tag')

    tags = association_proxy(
        'gametags', 'name', creator=lambda name: Tag.find_or_create(name)
    )


class Tag(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    @classmethod
    def find_or_create(cls, name):
        tag = cls.query.filter(cls.name == name).first()
        if tag is None:
            tag = Tag(name=name)
            db.session.add(tag)
        return tag


class GameTag(db.Model):
    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey(Game.id))
    tag_id = Column(Integer, ForeignKey(Tag.id))


class SQLAGameRepo(GameRepo):

    @inject
    def __init__(self, session: Session) -> None:
        self.session = session

    def fetch(self, id: int) -> GameEntity:
        game = self.session.query(Game).get(id)
        if game is None:
            raise Exception('Game not found!!!!')
        return self._convert_to_domain(game)

    def fetch_all(self) -> List[GameEntity]:
        return [
            self._convert_to_domain(g)
            for g in self.session.query(Game).order_by(Game.id).all()
        ]

    def add(self, game: GameEntity) -> None:
        self.session.add(self._convert_to_model(game))

    def remove(self, game: GameEntity) -> None:
        self.session.delete(self.fetch(game.id))

    def by_name(self, name: str) -> Optional[GameEntity]:
        game = self.session.query(Game).filter(Game.name == name).first()
        if not game:
            return None
        return self._convert_to_domain(game)

    def _convert_to_domain(self, game: Game) -> GameEntity:
        return GameEntity(
            id=game.id,
            name=game.name,
            description=game.description,
            min_players=game.min_players,
            max_players=game.max_players,
            age=game.age,
            tags=[GameTag_(name=t) for t in game.tags]
        )

    def _convert_to_model(self, game: GameEntity) -> Game:
        return Game(
            name=game.name,
            description=game.description,
            min_players=game.min_players,
            max_players=game.max_players,
            age=game.age,
            tags=[t for t in game.tags]
        )

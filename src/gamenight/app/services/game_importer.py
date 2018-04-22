from typing import List

from boardgamegeek import BoardGameGeek
from injector import inject
from sqlalchemy.orm import Session

from ...core.entities.game import Game
from ...core.repository.games import GameRepo
from ...core.services.importer import (GameImporter, RemoteGame,
                                       RemoteGameSearch)

BGGGameIdType = int


class BoardGameGeekSearch(RemoteGameSearch[BGGGameIdType]):

    @inject
    def __init__(self, client: BoardGameGeek) -> None:
        self.client = client

    def search(self, query: str) -> List[RemoteGame[BGGGameIdType]]:
        if not query:
            return []
        return [
            RemoteGame(id=r.id, name=r.name)
            for r in self.client.search(query)
        ]

    def retrieve(self, id: BGGGameIdType) -> Game:
        result = self.client.game(game_id=id)
        return self._convert_to_game(result)

    def _convert_to_game(self, item):
        return Game(
            name=item.name,
            min_players=item.min_players,
            max_players=item.max_players,
            age=item.min_age,
            tags=item.mechanics,
            description=item.description,
        )


class BoardGameGeekImporter(GameImporter[BGGGameIdType]):

    @inject
    def __init__(
            self, client: BoardGameGeek, repo: GameRepo, session: Session
    ) -> None:
        self.client = client
        self.repo = repo
        self.session = session

    def import_game(self, id: BGGGameIdType) -> Game:
        result = self.client.game(game_id=id)

        exists = self.repo.by_name(result.name)
        if exists:
            return exists

        game = self._convert_to_game(result)
        self.repo.add(game)
        self.session.commit()
        return game



    def _convert_to_game(self, item):
        return Game(
            name=item.name,
            min_players=item.min_players,
            max_players=item.max_players,
            age=item.min_age,
            tags=item.mechanics,
            description=item.description,
        )

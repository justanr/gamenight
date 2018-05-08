from typing import List

from boardgamegeek import BoardGameGeek
from injector import inject

from ...core.entities.game import Game
from ...core.services.remote import RemoteGame, RemoteGameSearch

BGGGameIdType = int


class BoardGameGeekSearch(RemoteGameSearch[BGGGameIdType]):

    @inject
    def __init__(self, client: BoardGameGeek) -> None:
        self.client = client

    def search(self, query: str) -> List[RemoteGame[BGGGameIdType]]:
        if not query:
            return []
        return [RemoteGame(id=r.id, name=r.name) for r in self.client.search(query)]

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

from injector import inject

from ..entities.game import Game
from ..repository.uow import UnitOfWorkManager
from .remote import GameImporter, RemoteGameIDType, RemoteGameSearch


class DefaultGameImporter(GameImporter):

    @inject
    def __init__(
            self, uowm: UnitOfWorkManager, search: RemoteGameSearch
    ) -> None:
        self._uowm = uowm
        self._search = search

    def import_game(self, id: RemoteGameIDType) -> Game:
        game = self._search.retrieve(id)

        with self._uowm.start() as uow:
            exists = uow.games.by_name(game.name)

            if exists:
                return exists

            uow.games.add(game)
            uow.commit()
            return game

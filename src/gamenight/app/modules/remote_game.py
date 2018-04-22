from ...core.services.importer import GameImporter, RemoteGameSearch
from injector import provider
from ..services.game_importer import BoardGameGeekSearch, BoardGameGeekImporter
from boardgamegeek import BoardGameGeek
from ._helpers import GamenightModule


class RemoteGameModule(GamenightModule):
    def configure(self, binder):
        binder.bind(GameImporter, BoardGameGeekImporter)
        binder.bind(RemoteGameSearch, BoardGameGeekSearch)

    @provider
    def boardgamegeek(self) -> BoardGameGeek:
        return BoardGameGeek()

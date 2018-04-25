from boardgamegeek import BoardGameGeek
from injector import provider

from ...core.services.importer import DefaultGameImporter
from ...core.services.remote import GameImporter, RemoteGameSearch
from ..services.game_importer import BoardGameGeekSearch
from ._helpers import GamenightModule


class RemoteGameModule(GamenightModule):

    def configure(self, binder):
        binder.bind(GameImporter, DefaultGameImporter)
        binder.bind(RemoteGameSearch, BoardGameGeekSearch)

    @provider
    def boardgamegeek(self) -> BoardGameGeek:
        return BoardGameGeek()

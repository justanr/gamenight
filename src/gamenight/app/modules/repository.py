from injector import provider

from ...core.repository.games import GameRepo
from ..repository.game import SQLAGameRepo
from ._helpers import GamenightModule


class RepositoryModule(GamenightModule):

    def configure(self, binder):
        binder.bind(GameRepo, SQLAGameRepo)

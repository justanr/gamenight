from injector import provider

from ...core.repository.games import GameRepo
from ...core.repository.uow import UnitOfWorkManager
from ..extensions import db
from ..repository.game import SQLAGameRepo
from ..repository.uow import SQLAUnitOfWorkManager
from ._helpers import GamenightModule


class RepositoryModule(GamenightModule):

    def configure(self, binder):
        binder.bind(UnitOfWorkManager, SQLAUnitOfWorkManager)

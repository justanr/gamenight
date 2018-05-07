from ...core.repository.uow import UnitOfWorkManager
from ..repository.uow import SQLAUnitOfWorkManager
from ._helpers import GamenightModule


class RepositoryModule(GamenightModule):

    def configure(self, binder):
        binder.bind(UnitOfWorkManager, SQLAUnitOfWorkManager)

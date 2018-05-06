from functools import wraps
from typing import Callable, ClassVar, Optional

from ...core.repository.uow import (UnitOfWork, UnitOfWorkError,
                                    UnitOfWorkManager)
from ..extensions import db
from .game import SQLAGameRepo


def _attach_repo(repo):
    return property(lambda self: repo())


class SQLAUnitOfWork(UnitOfWork):

    def open(self):
        pass

    def close(self):
        pass

    def commit(self):
        db.session.commit()

    def rollback(self):
        db.session.rollback()

    games = _attach_repo(SQLAGameRepo)


class SQLAUnitOfWorkManager(UnitOfWorkManager):
    configured: ClassVar[bool] = False

    def start(self) -> SQLAUnitOfWork:
        return SQLAUnitOfWork()

    @classmethod
    def configure(cls) -> None:
        if cls.configured:
            return

        super().configure()
        SQLAGameRepo.configure()

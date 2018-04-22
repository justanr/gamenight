from injector import provider
from sqlalchemy.orm import Session
from ._helpers import GamenightModule

from ..extensions import db


class ExtensionsModule(GamenightModule):
    @provider
    def provide_session(self) -> Session:
        return db.session

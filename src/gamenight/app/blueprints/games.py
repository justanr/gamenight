import attr
from flask import Response
from flask.views import MethodView
from injector import inject

from ...core.repository.uow import UnitOfWorkManager
from ..serialization import GameSchema, serialize_with
from ._helpers import GamenightBlueprint

games = GamenightBlueprint("games", __name__, url_prefix="/games")


class GamesView(MethodView):

    @inject
    def __init__(self, uowm: UnitOfWorkManager) -> None:
        self.uowm = uowm

    @serialize_with(schema=GameSchema, many=True)
    def get(self):
        with self.uowm.start() as uow:
            games = uow.games.fetch_all()

        return games, 200


class SpecificGameView(MethodView):

    @inject
    def __init__(self, uowm: UnitOfWorkManager) -> None:
        self.uowm = uowm

    @serialize_with(schema=GameSchema)
    def get(self, id: int) -> Response:
        with self.uowm.start() as uow:
            game = uow.games.fetch(id)

        return game


games.add_url_rule("/", view_func=GamesView.as_view("all"))
games.add_url_rule("/<int:id>", view_func=SpecificGameView.as_view("specific"))

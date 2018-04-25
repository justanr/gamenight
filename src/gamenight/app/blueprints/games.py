import attr
from flask import Response, jsonify
from flask.views import MethodView
from injector import inject

from ...core.repository.uow import UnitOfWorkManager
from ._helpers import GamenightBlueprint

games = GamenightBlueprint('games', __name__, url_prefix='/games')


class GamesView(MethodView):

    @inject
    def __init__(self, uowm: UnitOfWorkManager) -> None:
        self.uowm = uowm

    def get(self):
        with self.uowm.start() as uow:
            games = uow.games.fetch_all()

        return jsonify({
            'metadata': {
                'total': len(games)
            },
            'games': [attr.asdict(g) for g in games],
        })


class SpecificGameView(MethodView):

    @inject
    def __init__(self, uowm: UnitOfWorkManager) -> None:
        self.uowm = uowm

    def get(self, id: int) -> Response:
        with self.uowm.start() as uow:
            game = uow.games.fetch(id)

        return jsonify({'game': attr.asdict(game)})


games.add_url_rule('/', view_func=GamesView.as_view('all'))
games.add_url_rule('/<int:id>', view_func=SpecificGameView.as_view('specific'))

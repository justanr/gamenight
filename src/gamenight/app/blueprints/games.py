import attr
from flask import Response, jsonify
from flask.views import MethodView
from injector import inject

from ...core.repository.games import GameRepo
from ._helpers import GamenightBlueprint

games = GamenightBlueprint('games', __name__, url_prefix='/games')


class GamesView(MethodView):

    @inject
    def __init__(self, games: GameRepo) -> None:
        self.games = games

    def get(self):
        games = self.games.fetch_all()
        return jsonify({
            'metadata': {
                'total': len(games)
            },
            'games': [attr.asdict(g) for g in games],
        })


class SpecificGameView(MethodView):

    @inject
    def __init__(self, games: GameRepo) -> None:
        self.games = games

    def get(self, id: int) -> Response:
        game = self.games.fetch(id)
        return jsonify({'game': attr.asdict(game)})


games.add_url_rule('/', view_func=GamesView.as_view('all'))
games.add_url_rule('/<int:id>', view_func=SpecificGameView.as_view('specific'))

import attr
from flask import jsonify, request
from flask.views import MethodView
from injector import inject

from ...core.services.importer import GameImporter, RemoteGameSearch
from ._helpers import GamenightBlueprint
from ..serialization import GameSchema, serialize_with

external = GamenightBlueprint('external', __name__, url_prefix='/external')


class ExternalGameSearch(MethodView):

    @inject
    def __init__(self, search: RemoteGameSearch) -> None:
        self.remote_search = search

    def get(self):
        q = request.args.get('q')
        results = self.remote_search.search(q)
        return jsonify({
            'metadata': {
                'query': q,
                'total': len(results)
            },
            'results': [attr.asdict(r) for r in results]
        })


class RemoteGameView(MethodView):

    @inject
    def __init__(self, search: RemoteGameSearch) -> None:
        self.remote_search = search

    def get(self, id):
        return jsonify({'game': attr.asdict(self.remote_search.retrieve(id))})


class RemoteGameImport(MethodView):

    @inject
    def __init__(self, importer: GameImporter) -> None:
        self.importer = importer

    @serialize_with(schema=GameSchema)
    def post(self, id):
        return self.importer.import_game(id)


external.add_url_rule('/', view_func=ExternalGameSearch.as_view('search'))
external.add_url_rule('/<int:id>', view_func=RemoteGameView.as_view('view'))
external.add_url_rule('/import/<int:id>', view_func=RemoteGameImport.as_view('import'))

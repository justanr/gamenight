from ...core.entities.game import Game
from ...core.repository.games import GameSearchParams
from marshmallow_annotations import AnnotationSchema
from marshmallow import post_load, pre_load


class GameSchema(AnnotationSchema):
    class Meta:
        target = Game
        register_as_scheme = True


class GameSearchParamsSchema(AnnotationSchema):

    @post_load
    def make_obj(self, data):
        return GameSearchParams(**data)

    class Meta:
        target = GameSearchParams

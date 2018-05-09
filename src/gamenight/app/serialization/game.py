from marshmallow import post_load
from marshmallow_annotations import AnnotationSchema

from ...core.entities.game import Game
from ...core.repository.game import GameSearchParams


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

        class Fields:
            age = {"required": False, "allow_none": True}
            players = {"required": False, "allow_none": True}
            tags = {"required": False, "allow_none": True}

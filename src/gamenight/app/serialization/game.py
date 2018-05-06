from ...core.entities.game import Game
from marshmallow_annotations import AnnotationSchema


class GameSchema(AnnotationSchema):
    class Meta:
        target = Game
        register_as_scheme = True

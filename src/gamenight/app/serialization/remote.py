from marshmallow_annotations import AnnotationSchema
from ..services.game_importer import

class RemoteGameSchema(AnnotationSchema):
    class Meta:
        target = RemoteGame
        register_as_schema = True

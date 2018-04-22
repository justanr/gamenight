from .app.extensions import db
from .app.factory import make_app


app = make_app()

with app.app_context():
    db.create_all()

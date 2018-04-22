from flask import Flask
from flask_injector import FlaskInjector

from . import blueprints, modules
from .blueprints import GamenightBlueprint
from .extensions import db
from .modules import GamenightModule


def make_app():
    app = Flask('gamenight.app')
    configure_app(app)
    initialize_extensions(app)
    register_blueprints(app)
    finalize(app)
    return app


def configure_app(app):
    print("Configuring app...")
    app.config['SQLALCHEMY_DATABASE_URI'
               ] = 'sqlite:////home/anr/projects/gamenight/games.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


def initialize_extensions(app):
    print("Configuring extensions...")
    db.init_app(app)


def register_blueprints(app):
    print("Registering blueprints...")
    bps = [
        bp for bp in blueprints.__dict__.values()
        if isinstance(bp, GamenightBlueprint)
    ]
    for bp in bps:
        print(f'registering {bp}')
        app.register_blueprint(bp)


def finalize(app):
    print("Finalizing app...")
    print(f"Modules: {GamenightModule.__subclasses__()}")
    FlaskInjector(app, modules=GamenightModule.__subclasses__())

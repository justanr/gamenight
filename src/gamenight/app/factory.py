import ast
import os

from flask import Flask
from flask_injector import FlaskInjector

from . import blueprints, modules
from .blueprints import GamenightBlueprint
from .extensions import db
from .modules import GamenightModule


def make_app(config_path=None, instance_path=None):
    app = Flask('gamenight', instance_path=instance_path)
    setup_instance_path(app)
    configure_app(app, config_path)
    initialize_extensions(app)
    register_blueprints(app)
    finalize(app)
    return app


def setup_instance_path(app):
    if not os.path.exists(app.instance_path):
        os.makedirs(app.instance_path)


def configure_app(app, config_path=None):
    sources = app.config['CONFIG_SOURCES'] = {
        'default': 'gamenight.app.config.DefaultGameNightConfig',
        'envvar': 'GAMENIGHT_SETTINGS',
        'config_path': config_path,
        'envvar_prefix': 'GAMENIGHT_'
    }
    app.config.from_object(sources['default'])
    app.config.from_envvar(sources['envvar'], silent=True)

    if isinstance(config_path, str):
        if os.path.exists(config_path):
            app.config.from_pyfile(config_path)
        elif os.path.sep not in config:
            app.config.from_object(config_path)

    app.config.update(
        config_from_env('GAMENIGHT_', frozenset(['GAMENIGHT_SETTINGS']))
    )


def config_from_env(prefix, ignore=frozenset()):
    config = {}
    for key, value in os.environ.items():
        if key.startswith(prefix):
            try:
                value = ast.literal_eval(value)
            except:
                pass
            config[key.replace(prefix, '')] = value
    return config


def initialize_extensions(app):
    db.init_app(app)


def register_blueprints(app):
    bps = [
        bp for bp in blueprints.__dict__.values()
        if isinstance(bp, GamenightBlueprint)
    ]
    for bp in bps:
        app.register_blueprint(bp)

def finalize(app):
    FlaskInjector(app, modules=GamenightModule.__subclasses__())

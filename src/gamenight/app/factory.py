import ast
import os
from pathlib import Path
from types import ModuleType

from flask import Flask
from flask_injector import FlaskInjector

from . import blueprints, modules
from ..core.repository.uow import UnitOfWorkManager
from .blueprints import GamenightBlueprint
from .config.find import config_from_env, config_from_path, getqualname
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
    # track these to help deduce configuration issues
    sources = app.config['CONFIG_SOURCES'] = {
        'default': 'gamenight.app.config.DefaultGameNightConfig',
        'envvar': 'GAMENIGHT_SETTINGS',
        'config_path': config_path,
        'envvar_prefix': 'GAMENIGHT_',
        'matched_envvars': ()
    }
    app.config.from_object(sources['default'])

    cfg = config_from_path(app, config_path)
    if cfg is not None:
        # add app configuration and update sources to reflect where we
        # actually got the config from otherwise it's going to be frustrating
        # to trackdown what is set by whom

        if isinstance(cfg, (str, Path)):
            sources['config_path'] = str(cfg)
            app.config.from_pyfile(cfg)
        else:
            sources['config_path'] = _getqualname(obj)
            app.config.from_object(cfg)

    # configure from the envvar after the explicit path
    # because its more likely that explicit path is part of
    # startup script and the envvar has been set to override it
    app.config.from_envvar(sources['envvar'], silent=True)

    # store what was actually pulled out of the envvar
    sources['envvar'] = os.environ.get(sources['envvar'])

    envvars = config_from_env(
        'GAMENIGHT_', ignore=frozenset(['GAMENIGHT_SETTINGS'])
    )
    app.config.update(envvars)

    # only store what keys we matched, these could have sensitive data
    # in them and that would be bad to report out accidentally
    sources['matched_envvars'] = tuple(envvars.keys())


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
    injector = FlaskInjector(app, modules=GamenightModule.__subclasses__())
    app.injector = injector.injector

    ctx = app.app_context()
    ctx.push()

    try:
        uowm = app.injector.get(UnitOfWorkManager)
        uowm.configure()
    finally:
        ctx.pop()

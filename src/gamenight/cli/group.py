import os
import sys

import click
from flask import __version__ as flask_version
from flask import current_app
from flask.cli import FlaskGroup, ScriptInfo, with_appcontext
from flask_alembic import Alembic, alembic_click

from .. import __version__
from ..app.extensions import db
from ..app.factory import make_app


def app_factory(script_info):
    config_path = getattr(script_info, 'config', None)
    instance_path = getattr(script_info, 'instance_path', None)
    click.echo(f"Config Path: {config_path} Instance Path: {instance_path}")
    app = make_app(config_path=config_path, instance_path=instance_path)
    Alembic(app=app)
    return app


def set_config(ctx, param, value):
    ctx.ensure_object(ScriptInfo).config = value


def set_instance_path(ctx, param, value):
    ctx.ensure_object(ScriptInfo).instance_path = value


def get_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    sys_ver = sys.version.split('\n')[0]
    click.echo(
        f"gamenight {__version__} using Flask {flask_version} on Python {sys_ver}",
        color=ctx.color
    )
    ctx.exit()


class GamenightGroup(FlaskGroup):
    pass


@click.group(
    cls=GamenightGroup,
    create_app=app_factory,
    add_version_option=False,
    invoke_without_command=True
)
@click.option(
    '--config',
    expose_value=False,
    callback=set_config,
    required=False,
    is_flag=False,
    is_eager=False,
    metavar="CONFIG",
    help="Specify the configuration file to use, may either be an absolute"
    "path to a file (e.g. /var/config/gamenight.cfg)  or a python import"
    "path (e.g. gamenight.app.config.DefaultConfig"
)
@click.option(
    '--instance',
    expose_value=False,
    callback=set_instance_path,
    required=False,
    is_flag=False,
    is_eager=False,
    metavar="PATH",
    help="Specifies the instance path to use. By default the folder 'instance'"
    "next to the gamenight package is assumed to be the instance path"
)
@click.option(
    "--version",
    expose_value=False,
    callback=get_version,
    is_flag=True,
    is_eager=True,
    help="Show gamenight version info"
)
@click.pass_context
def gamenight(ctx):
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@gamenight.command(
    'shell', short_help='Runs a shell in the context of gamenight'
)
@with_appcontext
def shell():
    """
    Attempts to run a shell using ipython/jupyter if installed, otherwise falls
    back to the regular python shell.
    """
    import code
    banner = f"Python {sys.version} on {sys.platform}\nInstance path: {current_app.instance_path}"  # noqa
    ctx = {"db": db}

    # Support the regular Python interpreter startup script if someone
    # is using it.
    startup = os.environ.get("PYTHONSTARTUP")
    if startup and os.path.isfile(startup):
        with open(startup, "r") as f:
            eval(compile(f.read(), startup, "exec"), ctx)

    ctx.update(current_app.make_shell_context())
    try:
        import IPython
        IPython.embed(banner1=banner, user_ns=ctx)
    except ImportError:
        code.interact(banner=banner, local=ctx)


gamenight.add_command(alembic_click, 'db')

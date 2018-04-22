import os
import sys

import click
from flask import current_app
from flask.cli import FlaskGroup, with_appcontext
from flask_alembic import Alembic, alembic_click

from ..app.factory import make_app
from ..app.extensions import db

alembic = Alembic()


def app_factory(script_info):
    app = make_app()
    alembic.init_app(app)
    return app


class GamenightGroup(FlaskGroup):
    pass


@click.group(
    cls=GamenightGroup,
    create_app=app_factory,
    add_version_option=False,
    invoke_without_command=True
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

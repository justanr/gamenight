import click
from flask.cli import FlaskGroup
from flask_alembic import Alembic, alembic_click

from ..app.factory import make_app

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


gamenight.add_command(alembic_click, 'db')

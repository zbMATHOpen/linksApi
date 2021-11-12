import sqlalchemy
from flask import Blueprint

from zb_links.db.models import db

schemabp = Blueprint("schema", __name__)


@schemabp.cli.command("add")
def add_schemas():

    connection = db.engine.connect()
    try:
        connection.execute("CREATE SCHEMA IF NOT EXISTS zb_links;")
    except sqlalchemy.exc.ProgrammingError:
        pass

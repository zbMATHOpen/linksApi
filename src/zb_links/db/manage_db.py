import sqlalchemy
from flask import Blueprint

from zb_links.db.models import db

managebp = Blueprint("manage_db", __name__)


# clears the database
@managebp.cli.command("drop_all")
def db_drop_all():
    db.drop_all()

    # drop alembic if exists
    connection = db.engine.connect()
    try:
        connection.execute("DROP TABLE alembic_version;")
    except sqlalchemy.exc.ProgrammingError:
        pass

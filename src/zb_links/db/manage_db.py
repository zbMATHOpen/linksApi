import sqlalchemy
from flask import Blueprint

from zb_links.db.models import db

managebp = Blueprint("manage_db", __name__)


# clears the database
@managebp.cli.command("drop_all")
def db_drop_all():

    connection = db.engine.connect()
    # drop view if exists
    try:
        connection.execute("DROP VIEW author_groups;")
    except sqlalchemy.exc.ProgrammingError:
        pass    

    # drop math_author_ids if exists
    try:
        connection.execute("DROP TABLE math_author_ids;")
    except sqlalchemy.exc.ProgrammingError:
        pass

    db.drop_all()

    # drop alembic if exists
    try:
        connection.execute("DROP TABLE alembic_version;")
    except sqlalchemy.exc.ProgrammingError:
        pass

import sqlalchemy

from zb_links.db.models import db


def add_schemas():

    connection = db.engine.connect()
    try:
        connection.execute("CREATE SCHEMA IF NOT EXISTS zb_links;")
    except sqlalchemy.exc.ProgrammingError:
        pass

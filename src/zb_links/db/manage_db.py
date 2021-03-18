from flask import Blueprint
from psycopg2 import sql

from zb_links.db.models import db

managebp = Blueprint("manage_db", __name__)


# clear the database
@managebp.cli.command("reset")
def db_reset():
    connection = db.engine.connect()

    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        connection.execute(
            sql.SQL("DROP TABLE IF EXISTS {};").format(sql.Identifier(table))
        )

    # drop alembic as well
    connection.execute("DROP TABLE IF EXISTS alembic_version;")

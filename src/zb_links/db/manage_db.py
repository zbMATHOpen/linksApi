from flask import Blueprint

from zb_links.db.models import db

managebp = Blueprint("manage_db", __name__)


# clears the database
@managebp.cli.command("drop_all")
def db_drop_all():
    db.drop_all()

    # drop alembic as well
    connection = db.engine.connect()
    try:
        connection.execute("DROP TABLE alembic_version;")
    except Exception:
        connection.execute("DROP TABLE IF EXISTS alembic_version;")

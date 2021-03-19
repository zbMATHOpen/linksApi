from flask import Blueprint
from psycopg2 import sql

from zb_links.db.models import db

managebp = Blueprint("manage_db", __name__)


# clears the database
# is necessary if a new install is performed 
# after a previous version had already populated
# the database
@managebp.cli.command("drop_all")
def db_drop_all():
    
    db.drop_all()

    # drop alembic as well
    connection = db.engine.connect()
    connection.execute("DROP TABLE IF EXISTS alembic_version;")

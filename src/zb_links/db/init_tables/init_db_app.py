
from flask import Flask
from flask_migrate import Migrate

from zb_links import configure_app, initialize_db
from zb_links.db.models import db
from zb_links.db.init_tables.seed_db import seed_all
from zb_links.db.init_tables.view import add_view
from zb_links.db.init_tables.schema import add_schemas
from zb_links.db.init_tables.extra_tables import add_tables


def create_app():
    app = Flask(__name__)
    Migrate(app, db)
    configure_app(app)
    initialize_db(app)

    @app.cli.command("seed_all")
    def init_seeding():
        seed_all()

    @app.cli.command("schema_add")
    def init_schema():
        add_schemas()

    @app.cli.command("view_add")
    def init_view():
        add_view()

    @app.cli.command("extra_tables_add")
    def init_extra_tables():
        add_tables()

    return app

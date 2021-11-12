
from flask import Flask
from flask_migrate import Migrate

from zb_links import configure_app, initialize_db
from zb_links.db.models import db
from zb_links.db.init_tables.seed_db import seed_all


def create_app():
    app = Flask(__name__)
    Migrate(app, db)
    configure_app(app)
    initialize_db(app)

    @app.cli.command("seed_all")
    def init_seeding():
        seed_all()

    return app

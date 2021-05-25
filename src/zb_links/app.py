# ------------------------------------------------------------------------------
# zbMATH links API (Flask + Swagger + Flask-RESTPlus)
# ------------------------------------------------------------------------------
import os

from flask import Blueprint, Flask
from flask_migrate import Migrate
from pkg_resources import get_distribution

from zb_links.api.link.links import ns as links_namespace
from zb_links.api.link.partners import ns as partners_namespace
from zb_links.api.link.source import ns as source_namespace
from zb_links.api.link.statistics_msc import ns as statistics_msc_namespace
from zb_links.api.link.statistics_years import ns as statistics_years_namespace
from zb_links.api.restx import api
from zb_links.db.manage_db import managebp
from zb_links.db.models import db
from zb_links.db.seed_db import seedbp
from zb_links.db.schema import schemabp


def configure_app(flask_app):
    default_config = {
        "FLASK_APP": "zb_links.app.py",
        # follow recommended settings to save memory
        # see https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "SWAGGER_UI_DOC_EXPANSION": "list",
        "RESTPLUS_VALIDATE": True,
        "RESTPLUS_MASK_SWAGGER": False,
        "ERROR_404_HELP": False,
        "DEBUG": False,
        "TESTING": False,
        "CSRF_ENABLED": True,
        "API_VERSION": get_distribution("zbmath_links_api").version,
        "SQLALCHEMY_DATABASE_URI": None,
        "ZBMATH_API_KEY": None,
    }
    flask_app.config.from_mapping(default_config)
    # Overwrite config with
    for key in default_config.keys():
        if key in os.environ:
            flask_app.config[key] = os.getenv(key)


def initialize_db(flask_app):
    db.init_app(flask_app)
    db.app = flask_app


def initialize_app(flask_app):
    configure_app(flask_app)

    flask_app.register_blueprint(seedbp)
    flask_app.register_blueprint(schemabp)
    flask_app.register_blueprint(managebp)

    blueprint = Blueprint("links_api", __name__, url_prefix="/links_api")
    api.init_app(blueprint)

    api.add_namespace(partners_namespace)
    api.add_namespace(links_namespace)
    api.add_namespace(source_namespace)
    api.add_namespace(statistics_msc_namespace)
    api.add_namespace(statistics_years_namespace)

    flask_app.register_blueprint(blueprint)


def create_app():
    application = Flask(__name__)

    Migrate(application, db)
    initialize_app(application)
    initialize_db(application)
    return application


if __name__ == "__main__":
    app = create_app()

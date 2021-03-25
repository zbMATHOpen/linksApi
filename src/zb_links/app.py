# ------------------------------------------------------------------------------
# zbMATH links API (Flask + Swagger + Flask-RESTPlus)
# ------------------------------------------------------------------------------

import configparser
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


config = configparser.ConfigParser()
config.read('config.ini')

def configure_app(flask_app):
    flask_app.config.from_object(config['app']['app_settings'])
    flask_app.config["FLASK_APP"] = "zb_links.app.py"

    # follow recommended settings to save memory
    # see https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    flask_app.config["SWAGGER_UI_DOC_EXPANSION"] = "list"
    flask_app.config["RESTPLUS_VALIDATE"] = True
    flask_app.config["RESTPLUS_MASK_SWAGGER"] = False
    flask_app.config["ERROR_404_HELP"] = False
    flask_app.config["API_VERSION"] = get_distribution("dlmfapi").version


def initialize_db(flask_app):
    db.init_app(flask_app)
    db.app = flask_app


def initialize_app(flask_app):
    configure_app(flask_app)

    flask_app.register_blueprint(seedbp)
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
    app = Flask(__name__)

    Migrate(app, db)
    initialize_app(app)
    initialize_db(app)
    return app


if __name__ == "__main__":
    app = create_app()

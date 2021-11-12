# ------------------------------------------------------------------------------
# zbMATH links API (Flask + Swagger + Flask-RESTPlus)
# ------------------------------------------------------------------------------

from flask import Blueprint, Flask

from zb_links import configure_app, initialize_db
from zb_links.api.link.links import ns as links_namespace
from zb_links.api.link.partners import ns as partners_namespace
from zb_links.api.link.source import ns as source_namespace
from zb_links.api.link.statistics_msc import ns as statistics_msc_namespace
from zb_links.api.link.statistics_years import ns as statistics_years_namespace
from zb_links.api.restx import api




def initialize_app(flask_app):
    configure_app(flask_app)

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

    initialize_app(application)
    initialize_db(application)
    return application


if __name__ == "__main__":
    app = create_app()


import os
from pkg_resources import get_distribution

from zb_links.db.models import db

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
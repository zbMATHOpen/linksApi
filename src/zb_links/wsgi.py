from zb_links import config
from zb_links.app import create_app as create_api_app
from zb_links.db.init_tables.init_db_app import create_app as create_db_app

try:
    flask_app = config["application"]["FLASK_APP"]

    if flask_app == "zb_links.app":
        application = create_api_app()
    if flask_app == "zb_links.db.init_tables.init_db_app.py":
        application = create_db_app()
    else:
        application = create_api_app()
except KeyError:
    application = create_api_app()

# ------------------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------------------

from zb_links.app import db_uri


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = db_uri


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

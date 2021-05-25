# ------------------------------------------------------------------------------
# Definition of the models
# ------------------------------------------------------------------------------

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Partner(db.Model):
    __tablename__ = "partner"
    __table_args__ = {"schema": "zb_links"}

    name = db.Column(db.String(), primary_key=True)
    scheme = db.Column(db.String())
    url = db.Column(db.String())

    sources = db.relationship(
        "Source", backref="partners", cascade="all, delete-orphan"
    )

    def __init__(self, name, scheme, url):
        self.name = name
        self.scheme = scheme
        self.url = url


class Provider(db.Model):
    __tablename__ = "provider"
    __table_args__ = {"schema": "zb_links"}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    scheme = db.Column(db.String())
    url = db.Column(db.String())

    def __init__(self, id, name, scheme, url):
        self.id = id
        self.name = name
        self.scheme = scheme
        self.url = url


class Link(db.Model):
    __tablename__ = "document_external_ids"

    id = db.Column(db.Integer, primary_key=True)
    document = db.Column(
        db.Integer, db.ForeignKey("math_documents.id", onupdate="CASCADE")
    )
    external_id = db.Column(db.String())
    type = db.Column(db.String())
    matched_by = db.Column(db.String())
    created_at = db.Column(db.DateTime)
    created_by = db.Column(db.String())
    matched_at = db.Column(db.DateTime)
    parent_id = db.Column(
        db.Integer, db.ForeignKey("document_external_ids.id")
    )


class ZBTarget(db.Model):
    __tablename__ = "math_documents"

    id = db.Column(db.Integer, primary_key=True)
    zbl_id = db.Column(db.String())
    type = db.Column(db.String())
    title = db.Column(db.String())
    year = db.Column(db.String())
    source = db.Column(db.String())
    author = db.Column(db.String())
    classification = db.Column(db.String())


class Source(db.Model):
    __tablename__ = "source"
    __table_args__ = {"schema": "zb_links"}

    id = db.Column(db.String(), primary_key=True)
    id_scheme = db.Column(db.String())
    type = db.Column(db.String())
    url = db.Column(db.String())
    title = db.Column(db.String())
    partner = db.Column(
        db.String(), db.ForeignKey("zb_links.partner.name", onupdate="CASCADE")
    )

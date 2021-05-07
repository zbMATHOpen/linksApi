# ------------------------------------------------------------------------------
# Definition of the models
# ------------------------------------------------------------------------------

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Partner(db.Model):
    __tablename__ = "zb_links.partner"

    name = db.Column(db.String(), primary_key=True)
    scheme = db.Column(db.String())
    url = db.Column(db.String())

    links = db.relationship(
        "Link",
        backref="partner_link",
        cascade="all, delete-orphan"
    )

    sources = db.relationship(
        "Source",
        backref="partner_source",
        cascade="all, delete-orphan"
    )

    def __init__(
            self,
            name,
            scheme,
            url
    ):
        self.name = name
        self.scheme = scheme
        self.url = url


class Provider(db.Model):
    __tablename__ = "zb_links.provider"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    scheme = db.Column(db.String())
    url = db.Column(db.String())

    def __init__(
            self,
            id,
            name,
            scheme,
            url
    ):
        self.id = id
        self.name = name
        self.scheme = scheme
        self.url = url

    links = db.relationship(
        "Link",
        backref="provider_link",
        cascade="all, delete-orphan"
    )


class Link(db.Model):
    __tablename__ = "document_external_ids"

    id = db.Column(db.Integer, primary_key=True)
    document = db.Column(
        db.Integer,
        db.ForeignKey("math_documents.id", onupdate="CASCADE")
    )
    external_id = db.Column(db.String())
    type = db.Column(
        db.String(),
        db.ForeignKey("zb_links.partner.name", onupdate="CASCADE")
    )
    created_at = db.Column(db.DateTime)
    created_by = db.Column(
        db.Integer,
        db.ForeignKey("zb_links.provider.id", onupdate="CASCADE")
    )
    matched_at = db.Column(db.DateTime)
    parent_id = db.Column(
        db.Integer,
        db.ForeignKey("document_external_ids.id")
    )

    def __init__(
            self,
            id,
            document,
            external_id,
            type,
            created_at,
            created_by,
            matched_at
    ):
        self.id = id
        self.document = document
        self.external_id = external_id
        self.type = type
        self.created_at = created_at
        self.created_by = created_by
        self.matched_at = matched_at


class ZBTarget(db.Model):
    __tablename__ = "math_documents"

    id = db.Column(db.String())
    zbl_id = db.Column(db.String(), primary_key=True)
    type = db.Column(db.String())
    title = db.Column(db.String())
    year = db.Column(db.String())
    source = db.Column(db.String())
    author = db.Column(db.String())
    classification = db.Column(db.String())


class Source(db.Model):
    __tablename__ = "zb_links.source"

    id = db.Column(db.String(), primary_key=True)
    id_scheme = db.Column(db.String())
    type = db.Column(db.String())
    url = db.Column(db.String())
    title = db.Column(db.String())
    partner = db.Column(
        db.String(),
        db.ForeignKey("zb_links.partner.name", onupdate="CASCADE")
    )

    def __init__(
            self,
            id,
            id_scheme,
            type,
            url,
            title,
            partner
    ):
        self.id = id
        self.id_scheme = id_scheme
        self.type = type
        self.url = url
        self.title = title
        self.partner = partner

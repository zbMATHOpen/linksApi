# ------------------------------------------------------------------------------
# Defition of the models
# ------------------------------------------------------------------------------

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Partner(db.Model):
    __tablename__ = "zbmath_partners"
    __table_args__ = (db.UniqueConstraint("name"),)

    partner_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True)
    scheme = db.Column(db.String())
    url = db.Column(db.String())

    # Partner-Link, Partner-Source are one-to-many relationships
    links = db.relationship(
        "Link", backref="link_partner", cascade="all, delete-orphan"
    )
    sources = db.relationship(
        "Source", backref="source_partner", cascade="all, delete-orphan"
    )

    def __init__(self, partner_id, name, scheme, url):
        self.partner_id = partner_id
        self.name = name
        self.scheme = scheme
        self.url = url


class Provider(db.Model):
    __tablename__ = "provider_table"

    provider_id = db.Column(db.Integer, primary_key=True)
    provider_name = db.Column(db.String())
    id_scheme = db.Column(db.String())
    provider_url = db.Column(db.String())

    def __init__(self, provider_id, provider_name, id_scheme, provider_url):
        self.provider_id = provider_id
        self.provider_name = provider_name
        self.id_scheme = id_scheme
        self.provider_url = provider_url


class Link(db.Model):
    __tablename__ = "link_table"
    __table_args__ = (
        db.UniqueConstraint(
            "source_id",
            "target_id",
            "partner_id",
            name="link_unique_constraint",
        ),
    )

    link_id = db.Column(db.Integer, primary_key=True)

    source_id = db.Column(
        db.Integer, db.ForeignKey("source_table.source_id", onupdate="CASCADE")
    )
    source_identifier = db.Column(
        db.String()
    )  # must manually update if changed;
    # partner object identifier, e.g. dlmf url suffix
    target_id = db.Column(
        db.String(),
        db.ForeignKey("zb_target_table.zbl_code", onupdate="CASCADE"),
    )  # zbl_code
    partner_id = db.Column(db.Integer)
    partner_name = db.Column(
        db.String(), db.ForeignKey("zbmath_partners.name", onupdate="CASCADE")
    )
    link_publication_date = db.Column(db.DateTime)
    link_provider = db.Column(
        db.Integer,
        db.ForeignKey("provider_table.provider_id", onupdate="CASCADE"),
    )  # provider_id
    link_added_date = db.Column(db.DateTime)  # date when zb_math adds to db
    relationship_type = db.Column(db.String())


class Source(db.Model):
    __tablename__ = "source_table"
    __table_args__ = (
        db.UniqueConstraint(
            "identifier", "partner", name="source_unique_constraint"
        ),
    )

    source_id = db.Column(db.Integer, primary_key=True)

    identifier = db.Column(db.String())  # e.g. dlmf url suffix
    id_scheme = db.Column(db.String())
    type_name = db.Column(db.String())
    url = db.Column(
        db.String()
    )  # url where link occurs (e.g. using url suffix)
    title = db.Column(db.String())  # e.g. title of DLMF section
    partner = db.Column(
        db.String(), db.ForeignKey("zbmath_partners.name", onupdate="CASCADE")
    )  # zbMATH partner

    # Source-Link is a one-to-many relationship
    links = db.relationship(
        "Link", backref="link_source", cascade="all, delete-orphan"
    )

    def __init__(
        self, source_id, identifier, id_scheme, type_name, url, title, partner
    ):
        self.source_id = source_id
        self.identifier = identifier
        self.id_scheme = id_scheme
        self.type_name = type_name
        self.url = url
        self.title = title
        self.partner = partner


# connects author_ids and zb_documents
doc_author = db.Table(
    "doc_author",
    db.Column(
        "author_id", db.String(), db.ForeignKey("author_id_table.author_id")
    ),
    db.Column(
        "zbl_code", db.String(), db.ForeignKey("zb_target_table.zbl_code")
    ),
)


class ZBTarget(db.Model):
    __tablename__ = "zb_target_table"

    zbl_code = db.Column(db.String(), primary_key=True)
    id_scheme = db.Column(db.String())
    type_name = db.Column(db.String())
    title = db.Column(db.String())
    publication_date = db.Column(
        db.Integer
    )  # year of publication in journal/book
    source_of_publication = db.Column(db.String())  # source col of matrix db
    authors = db.Column(db.String())
    msc = db.Column(db.String())

    # Target-Link is a one-to-many relationship
    links = db.relationship(
        "Link", backref="target", cascade="all, delete-orphan"
    )

    # Target-AuthorId is a many-to-many relationship
    author_ids = db.relationship(
        "AuthorId",
        secondary=doc_author,
        back_populates="zb_docs",
        lazy="dynamic",
    )

    def __init__(
        self,
        zbl_code,
        id_scheme,
        type_name,
        title,
        publication_date,
        source_of_publication,
        authors,
        msc,
    ):
        self.zbl_code = zbl_code
        self.id_scheme = id_scheme
        self.type_name = type_name  # e.g. math_documents entry
        self.title = title
        self.publication_date = publication_date
        self.source_of_publication = source_of_publication
        self.authors = authors
        self.msc = msc


# connects author_ids and author_names
auth_id_name = db.Table(
    "author_id_name",
    db.Column(
        "author_id", db.String(), db.ForeignKey("author_id_table.author_id")
    ),
    db.Column(
        "author_name",
        db.String(),
        db.ForeignKey("author_name_table.published_name"),
    ),
)


class AuthorId(db.Model):
    __tablename__ = "author_id_table"
    author_id = db.Column(db.String(), primary_key=True)

    # do not cascade delete; other author_ids can share name/doc
    author_names = db.relationship(
        "AuthorName",
        secondary=auth_id_name,
        back_populates="author_ids",
        lazy="dynamic",
    )
    zb_docs = db.relationship(
        "ZBTarget",
        secondary=doc_author,
        back_populates="author_ids",
        lazy="dynamic",
    )

    def __init__(self, author_id):
        self.author_id = author_id


class AuthorName(db.Model):
    __tablename__ = "author_name_table"
    published_name = db.Column(
        db.String(), primary_key=True
    )  # name which appears on a publication

    author_ids = db.relationship(
        "AuthorId",
        secondary=auth_id_name,
        back_populates="author_names",
        lazy="dynamic",
    )

    def __init__(self, name):
        self.published_name = name

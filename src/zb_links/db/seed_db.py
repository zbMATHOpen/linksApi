# ------------------------------------------------------------------------------
# Seeding the Database
# ------------------------------------------------------------------------------

import click
from flask import Blueprint

from zb_links.db.models import (
    AuthorId,
    AuthorName,
    Link,
    Partner,
    Provider,
    Source,
    ZBTarget,
    db,
)

seedbp = Blueprint("seed", __name__)


@seedbp.cli.command("partner")
def seed_partner():
    partner_id = 1
    name = "DLMF"
    scheme = "DLMF scheme"
    url = "https://dlmf.nist.gov/"

    new_partner = Partner(partner_id, name, scheme, url)

    db.session.add(new_partner)
    db.session.commit()


@seedbp.cli.command("provider")
def seed_provider():
    provider_id = 1
    name = "zbMATH"
    scheme = "zbMATH scheme"
    url = "https://zbmath.org/"

    new_provider = Provider(provider_id, name, scheme, url)

    db.session.add(new_provider)
    db.session.commit()


@seedbp.cli.command("source")
def seed_source():
    source_id = 1
    source_identifier = "11.14#I1.i1.p1"
    scheme = "DLMF scheme"
    type_name = "DLMF bibliographic entry"
    url = "https://dlmf.nist.gov/11.14#I1.i1.p1"
    chapter_title = (
        "1st item ‣ §11.14(ii) Struve Functions ‣ "
        "§11.14 Tables ‣ Computation ‣ "
        "Chapter 11 Struve and Related Functions"
    )
    partner = "DLMF"

    new_source_entry = Source(
        source_id,
        source_identifier,
        scheme,
        type_name,
        url,
        chapter_title,
        partner,
    )

    db.session.add(new_source_entry)
    db.session.commit()


@seedbp.cli.command("target")
def seed_target():
    zbl_code = "0171.38503"
    id_scheme = "zbMATH scheme"
    type_name = "book"
    title = (
        "Handbook of mathematical functions with formulas, "
        "graphs and mathematical tables"
    )
    publication_date = "1964"
    source_of_publication = (
        "Washington: U.S. Department of Commerce. " "xiv, 1046 pp. (1964)."
    )
    authors = "Abramowitz, Milton (ed.); Stegun, Irene A. (ed.)"
    msc_list = (
        "33-00 00A20 00A22 65A05 65Dxx 41A55 " "62Q05 44A10 11B68 11M06 11Y70"
    )

    new_target = ZBTarget(
        zbl_code,
        id_scheme,
        type_name,
        title,
        publication_date,
        source_of_publication,
        authors,
        msc_list,
    )

    db.session.add(new_target)
    db.session.commit()


@seedbp.cli.command("link")
def seed_link():
    # TODO: in general the partner can be read from below partner_name
    dlmf_partner_obj = Partner.query.filter_by(name="DLMF").first()

    target_id = "0171.38503"
    source_id = 1
    new_link = Link(
        link_id=1,
        source_id=source_id,
        source_identifier="11.14#I1.i1.p1",
        target_id=target_id,
        partner_id=1,
        partner_name="DLMF",
        link_publication_date="2010-01-01T00:00:00",
        link_provider=1,
        link_added_date="2010-01-01T00:00:00",
        relationship_type="equation referenced",
    )

    # add link to partner, target, and to source
    zb_target_obj = ZBTarget.query.filter_by(zbl_code=target_id).first()
    source_obj = Source.query.filter_by(source_id=source_id).first()

    dlmf_partner_obj.links.append(new_link)
    zb_target_obj.links.append(new_link)
    source_obj.links.append(new_link)

    db.session.add(new_link)
    db.session.commit()


@seedbp.cli.command("author_id")
def seed_author_id():
    author_id = "abramowitz.milton"
    new_author = AuthorId(author_id)

    db.session.add(new_author)
    db.session.commit()


@seedbp.cli.command("author_name")
def seed_author_name():
    name = "Abramowitz, Milton"
    new_author = AuthorName(name)

    db.session.add(new_author)
    db.session.commit()


@seedbp.cli.command("author_id_name")
def seed_author_id_name():
    author_id = "abramowitz.milton"
    name = "Abramowitz, Milton"

    author_with_id = AuthorId.query.get(author_id)
    author_with_name = AuthorName.query.get(name)

    author_with_id.author_names.append(author_with_name)
    db.session.commit()


@seedbp.cli.command("doc_author")
def seed_doc_author():
    author_id = "abramowitz.milton"
    doc_id = "0171.38503"

    zb_doc = ZBTarget.query.get(doc_id)
    author_with_id = AuthorId.query.get(author_id)

    author_with_id.zb_docs.append(zb_doc)
    db.session.commit()


@seedbp.cli.command("all")
@click.pass_context
def click_seed_all(ctx):
    seed_partner.invoke(ctx)
    seed_provider.invoke(ctx)
    seed_source.invoke(ctx)
    seed_target.invoke(ctx)
    seed_link.invoke(ctx)
    seed_author_id.invoke(ctx)
    seed_author_name.invoke(ctx)
    seed_author_id_name.invoke(ctx)
    seed_doc_author.invoke(ctx)

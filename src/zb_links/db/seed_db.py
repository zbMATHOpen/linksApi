# ------------------------------------------------------------------------------
# Seeding the Database
# ------------------------------------------------------------------------------

import click
from flask import Blueprint

from zb_links.db.models import (
    # AuthorId,
    # AuthorName,
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
    name = "DLMF"
    scheme = "DLMF scheme"
    url = "https://dlmf.nist.gov/"

    new_partner = Partner(name, scheme, url)

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
    chapter_title = (
        "1st item ‣ §11.14(ii) Struve Functions ‣ "
        "§11.14 Tables ‣ Computation ‣ "
        "Chapter 11 Struve and Related Functions"
    )

    new_source_entry = Source(
        id="11.14#I1.i1.p1",
        id_scheme="DLMF scheme",
        type="DLMF bibliographic entry",
        url="https://dlmf.nist.gov/11.14#I1.i1.p1",
        title=chapter_title,
        partner="DLMF",
    )
    
    # add source to partner
    partner_obj = Partner.query.filter_by(name="DLMF").first()
    partner_obj.sources.append(new_source_entry)

    db.session.add(new_source_entry)
    db.session.commit()


@seedbp.cli.command("target")
def seed_target():
    book_title = (
        "Handbook of mathematical functions with formulas, "
        "graphs and mathematical tables"
    )
    source_of_publication = (
        "Washington: U.S. Department of Commerce. " "xiv, 1046 pp. (1964)."
    )
    authors = "Abramowitz, Milton (ed.); Stegun, Irene A. (ed.)"
    msc_list = (
        "33-00 00A20 00A22 65A05 65Dxx 41A55 " "62Q05 44A10 11B68 11M06 11Y70"
    )

    new_target = ZBTarget(
        id=3273551,
        zbl_id="0171.38503",
        type="book",
        title=book_title,
        year="1964",
        source=source_of_publication,
        author=authors,
        classification=msc_list,
    )

    db.session.add(new_target)
    db.session.commit()


@seedbp.cli.command("link")
def seed_link():
    new_link = Link(
        id=1,
        document=3273551,
        external_id="11.14#I1.i1.p1",
        type="DLMF",
        matched_by="LinksApi",
        created_at="2010-01-01 00:00:00",
        created_by="Dariush, Matteo",
        matched_at="2021-01-01 00:00:00",
        parent_id=1,
    )

    db.session.add(new_link)
    db.session.commit()


@seedbp.cli.command("all")
@click.pass_context
def click_seed_all(ctx):
    seed_partner.invoke(ctx)
    seed_provider.invoke(ctx)
    seed_source.invoke(ctx)
    seed_target.invoke(ctx)
    seed_link.invoke(ctx)


# ------------------------------------------------------------------------------
# Seeding the Database
# ------------------------------------------------------------------------------

from datetime import datetime

import pytz

from zb_links.db.models import Link, Partner, Source, ZBTarget, db


def seed_partner():
    name = "dlmf"
    display_name = "DLMF"
    scheme = "DLMF scheme"
    url = "https://dlmf.nist.gov/"

    new_partner = Partner(name, display_name, scheme, url)

    db.session.add(new_partner)
    db.session.commit()


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
        partner="dlmf",
    )

    # add source to partner
    partner_obj = Partner.query.filter_by(name="dlmf").first()
    partner_obj.sources.append(new_source_entry)

    db.session.add(new_source_entry)
    db.session.commit()


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

    new_target = ZBTarget(
        id=2062129,
        zbl_id="1234.98765",
        type="serial_article",
        title="a title",
        year="1789",
        source="an older source",
        author="me",
        classification="12A34",
    )

    db.session.add(new_target)

    db.session.commit()


def seed_link():
    dt = datetime(2021, 1, 1)
    dt = dt.replace(tzinfo=pytz.timezone("Europe/Berlin"))
    # dt = datetime("2021-12-15", "%Y-%m-%d")
    new_link = Link(
        document=3273551,
        external_id="11.14#I1.i1.p1",
        type="dlmf",
        matched_by="zbmath-links-api",
        matched_by_version="0.2",
        matched_at=dt,
        created_by="api_user",
    )

    db.session.add(new_link)
    db.session.commit()


def seed_author_ids():
    connection = db.engine.connect()
    data_row = """
    INSERT INTO math_author_ids
    VALUES (1, 'Abramowitz, M.', 3273551, 1442);
    """
    connection.execute(data_row)


def seed_all():
    seed_partner()
    seed_source()
    seed_target()
    seed_link()
    seed_author_ids()

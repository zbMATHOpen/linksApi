from zb_links.api.link.helpers import dlmf_source_helpers, helpers
from zb_links.db.models import Source, db

Sources = {
    "DLMF": {
        "id_scheme": "DLMF scheme",
        "url_prefix": "https://dlmf.nist.gov/",
        "type": "DLMF reference",
    }
}


def create_new_source(source_val, source_name, title_name=None):
    if source_name == "DLMF":
        if not title_name:
            title_name = dlmf_source_helpers.get_title(source_val)

    try:
        url = Sources[source_name]["url_prefix"] + source_val
        new_source = Source(
            id=source_val,
            id_scheme=Sources[source_name]["id_scheme"],
            type=Sources[source_name]["type"],
            url=url,
            title=title_name,
            partner=source_name,
        )
        db.session.add(new_source)
        db.session.commit()
    except Exception as e:
        return helpers.make_message(409, str(e))

    return None


def edit_source_title(source_val, source_name, title_name):
    """
    Edits the title field in the zblinks.source table

    Parameters
    ----------
    source_val : str
        the id of the source.
    source_name : str
        name of the zbMATH partner.
    title_name : str
        title associated with the source id (source_val).

    Returns
    -------
    http code, 409, if error
    None otherwise

    """

    try:
        source = Source.query.filter_by(
            id=source_val, partner=source_name
        ).first()
        source.title = title_name
        db.session.commit()
    except Exception as e:
        return helpers.make_message(409, str(e))

    return None

from zb_links.api.link.helpers import helpers, dlmf_source_helpers
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
            partner=source_name
        )
        db.session.add(new_source)
        db.session.commit()
    except Exception as e:
        return helpers.make_message(409, str(e))

    return None

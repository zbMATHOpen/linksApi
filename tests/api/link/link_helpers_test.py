from unittest.mock import patch
from zb_links.api.link.helpers.link_helpers import get_author_objs
from zb_links.db.models import db, AuthorName


def test_author_query(client):
    author_1 = "Abramowitz, M."
    author_2 = "Abramowitz, Mi."

    author_1_objs = get_author_objs(author_1)
    author_2_objs = get_author_objs(author_2)

    for a_2 in author_2_objs[0]:
        assert a_2 in author_1_objs[0]



def test_author_query_with_bad_db(client):

    the_real_isaac = AuthorName("Newton, Sr. Isaac")
    db.session.add(the_real_isaac)
    db.session.commit()

    author = "Newton, Sreisaac"
    author_objs = get_author_objs(author)[0]

    isaac = AuthorName.query.filter_by(published_name="Newton, Sr. Isaac").first()
    db.session.delete(isaac)
    db.session.commit()

    assert len(author_objs) == 0


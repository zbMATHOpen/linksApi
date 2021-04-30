
from zb_links.api.link.helpers.link_helpers import get_author_objs
from zb_links.db.models import db, AuthorName


def test_author_query(client):
    author_1 = "Abramowitz, M."
    author_2 = "Abramowitz, Mi."

    author_1_objs = get_author_objs(author_1)
    author_2_objs = get_author_objs(author_2)

    for a_2 in author_2_objs[0]:
        assert a_2 in author_1_objs[0]


def test_last_name_author_query(client):
    author = "Abramowitz"

    author_objs = get_author_objs(author)

    assert len(author_objs[0]) > 0


def test_author_query_with_bad_db(client):

    the_real_isaac = AuthorName("Newton, Sr. Isaac")
    imposter_isaac = AuthorName("Newton,csSr.crIsaac")
    db.session.add(the_real_isaac)
    db.session.add(imposter_isaac)
    db.session.commit()

    author = "newton, sr. isaac"
    author_objs = get_author_objs(author)[0]

    isaac = AuthorName.query.filter_by(published_name="Newton, Sr. Isaac").first()
    db.session.delete(isaac)
    fake_isaac = AuthorName.query.filter_by(published_name="Newton,csSr.crIsaac").first()
    db.session.delete(fake_isaac)
    db.session.commit()

    assert len(author_objs) == 1


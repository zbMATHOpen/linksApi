
from zb_links.api.link.helpers.source_helpers import create_new_source
from zb_links.db.models import Source, db


def test_new_source_with_title():
    source_val = "26.8#vii.p4"
    source_name = "dlmf"
    title_name = "my cool title"

    response = create_new_source(source_val, source_name, title_name)
    assert not response

    test_source = Source.query.filter_by(id=source_val)
    assert test_source.one().title == "my cool title"

    # delete test entry
    test_source.delete()
    db.session.commit()


def test_new_source_wout_title():
    source_val = "26.8#vii.p4"
    source_name = "dlmf"

    response = create_new_source(source_val, source_name)
    assert not response

    test_source = Source.query.filter_by(id=source_val)
    assert test_source.one().title

    # delete test entry
    test_source.delete()
    db.session.commit()


from zb_links.api.link.helpers.link_helpers import get_links_from_author


def test_author_query(client):
    author_1 = "Abramowitz, M."
    author_2 = "Abramowitz, Mi."

    author_1_links = get_links_from_author(author_1)
    author_2_links = get_links_from_author(author_2)

    for link_2 in author_2_links:
        assert link_2 in author_1_links


def test_last_name_author_query(client):
    author = "Abramowitz"

    author_links = get_links_from_author(author)

    assert len(author_links) > 0





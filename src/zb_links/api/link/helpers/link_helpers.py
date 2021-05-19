from sqlalchemy import func, or_, text

from zb_links.db.models import Link, ZBTarget, db
import re


def update_set(old_set, new_set):
    if not old_set:
        return new_set
    return set.intersection(old_set, new_set)


def nontrivial(name_list):
    nontrivial_length = 0
    for name in name_list:
        reduced_name = re.sub("[^A-Za-z]+", "", name)
        nontrivial_length += len(reduced_name)
    return nontrivial_length > 0


def get_author_expressions(author):
    """

    Parameters
    ----------
    author : str
        name of author(s) from user search input.

    Returns
    -------
    author_exp_list: list of regular expressions
        each expression in the list will be used to search
        for an author

    """

    # remove possible double spaces from input
    author = re.sub(" +", " ", author)

    author_exp_list = []
    author_list = author.split(";")
    for an_author in author_list:
        an_author = an_author.strip()
        an_author_pieces = an_author.split(" ")

        last_name = an_author_pieces[0]
        remaining_names = an_author_pieces[1:]
        if nontrivial(remaining_names):
            an_author_expression = last_name + " "

            remaining_names = an_author_pieces[1:]
            for a_piece in remaining_names:
                a_piece = a_piece.strip(".")

                an_author_expression += a_piece + "% "
        else:
            an_author_expression = last_name + "%"

        an_author_expression = an_author_expression.strip().lower()
        author_exp_list.append(an_author_expression)

    return author_exp_list


def get_links_from_author(author):
    """

    Parameters
    ----------
    author : str
        name of author(s) from user search input.

    Returns
    -------
    link_list_auth : list of Link objects
        returns all Links associated to
        ZBTarget documents which are associated to all
        AuthorIds associated to all authors in search input.

    """

    author_expressions = get_author_expressions(author)

    doc_id_list = []
    connection = db.engine.connect()
    for each_exp in author_expressions:
        auth_doc_query = text("""
            SELECT document
            FROM author_groups
            WHERE LOWER(name) LIKE :a_name;
        """
        )

        query_results = connection.execute(auth_doc_query, a_name=each_exp)

        # query_results = connection.execute(text(auth_doc_query))
        author_documents = set(query_results)

        auth_doc_list = [doc_el[0] for doc_el in author_documents]
        doc_id_list.append(auth_doc_list)

    # get intersection of doc ids belonging to each author set
    intersection_docs = set(doc_id_list[0])
    for doc_list in doc_id_list:
        intersection_docs = set.intersection(set(doc_list), intersection_docs)

    link_list_auth = [
        link
        for doc in intersection_docs
        for link in set(Link.query.filter(Link.document==doc,
                                          Link.matched_by=='LinksApi')
                        .all()
                        )
        ]

    return link_list_auth


def get_links_from_mscs(msc_val):
    """

    Parameters
    ----------
    msc_val : str
        msc classification codes, multiple values are
        separated by spaces.

    Returns
    -------
    link_list_msc : list of Link objects
        returns all Links associated to
        ZBTarget documents which are associated to all
        to all msc codes in search input.

    """

    msc_query = ZBTarget.query
    msc_list = msc_val.split(" ")
    for an_msc in msc_list:
        an_msc = an_msc.strip()
        msc_with_empty = " " + an_msc
        msc_query = msc_query.filter(
            or_(
                func.lower(ZBTarget.classification).startswith(an_msc),
                func.lower(ZBTarget.classification).contains(msc_with_empty),
            )
        )

    msc_docs_ids = [doc.id for doc in msc_query]

    link_query = Link.query.filter(Link.document.in_(msc_docs_ids))

    link_list_msc = [link for link in link_query.all()]

    return link_list_msc

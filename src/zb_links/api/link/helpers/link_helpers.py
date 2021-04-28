from sqlalchemy import func, or_

from zb_links.db.models import AuthorName, Link, ZBTarget
import re


def get_author_objs(author):
    """

    Parameters
    ----------
    author : str
        name of author from user search input.

    Returns
    -------
    author_name_objs : list of list of AuthorName objects
        for each author in input a list of AuthorName objects
        associated with that author is created. Final list is the
        list of AuthorName lists

    """
    author_name_query = AuthorName.query
    author_name_objs = []

    # remove possible double spaces from input
    author = re.sub(" +", " ", author)

    author_list = author.split(";")
    for an_author in author_list:
        an_author = an_author.strip()
        an_author_pieces = an_author.split(" ")

        last_name = an_author_pieces[0]
        an_author_expression = last_name + " "

        remaining_names = an_author_pieces[1:]
        for a_piece in remaining_names:
            a_piece = a_piece.strip(".")

            an_author_expression += a_piece + "% "

        an_author_expression = an_author_expression.strip()

        author_names = author_name_query.filter(
            func.lower(AuthorName.published_name).like(an_author_expression)
        ).all()

        author_name_objs.append(list(author_names))

    return author_name_objs


def get_links_from_author(author):
    """

    Parameters
    ----------
    author : str
        name of author from user search input.

    Returns
    -------
    link_list_auth : list of Link objects
        returns all Links associated to
        ZBTarget documents which are associated to all
        AuthorIds associated to all authors in search input.

    """

    author_name_objs = get_author_objs(author)

    # create sets of ids, assoc. with each author_name entry
    author_id_objs = []
    for name_list in author_name_objs:
        name_id_list = []
        for a_name in name_list:
            name_id_list.extend(a_name.author_ids)
        author_id_objs.append(name_id_list)

    # get docs which belong to all id sets
    target_objs_list = []
    for id_list in author_id_objs:
        id_doc_list = []
        for auth_id in id_list:
            id_doc_list.extend(auth_id.zb_docs)
        target_objs_list.append(id_doc_list)

    # get intersection of docs belonging to each set of ids
    intersection_docs = set(target_objs_list[0])
    for doc_list in target_objs_list:
        intersection_docs = set.intersection(set(doc_list), intersection_docs)

    link_list_auth = [link for doc in intersection_docs for link in doc.links]

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
                func.lower(ZBTarget.msc).startswith(an_msc),
                func.lower(ZBTarget.msc).contains(msc_with_empty),
            )
        )

    msc_docs_codes = list([doc.zbl_code for doc in msc_query])

    link_query = Link.query.filter(Link.target_id.in_(msc_docs_codes))

    link_list_msc = [link for link in link_query.all()]

    return link_list_msc
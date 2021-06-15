# ------------------------------------------------------------------------------
# Link window (2 GET + 1 POST)
# ------------------------------------------------------------------------------

from datetime import datetime

from flask import request
from flask_restx import Resource, reqparse

from zb_links.api.link.display import get_display, link
from zb_links.api.link.helpers import helpers, link_helpers
from zb_links.api.restx import api, token_required
from zb_links.db.models import Link, Partner, Source, ZBTarget, db

ns = api.namespace(
    "link", description="Operations related to linking to zbMATH"
)

search_by_arguments = reqparse.RequestParser()

search_by_arguments.add_argument("author", type=str, required=False)

search_by_arguments.add_argument("classification", type=str, required=False)

search_by_arguments.add_argument("document", type=int, required=False)


@api.expect(search_by_arguments)
@ns.route("/")
class LinkCollection(Resource):
    @api.marshal_list_with(link)
    @api.doc(
        params={
            "author": {
                "description": "Ex: Abramowitz, M. "
                "(multiple inputs with ; as delimiter)"
            },
            "document": {
                "description": "Ex: 3273551 (DE number, available in the "
                "bibtex of each document at https://zbmath.org/)"
            },
            "classification": {
                "description": "Ex: 33-00 "
                "(MSC code, multiple inputs with space as "
                "delimiter) "
            },
        }
    )
    def get(self):
        """Retrieve links for given zbMATH objects"""
        args = request.args

        author = None
        msc_val = None
        de_val = None
        if "author" in args:
            author = args["author"].lower()
        if "classification" in args:
            msc_val = args["classification"].lower()
        if "document" in args:
            de_val = args["document"]

        link_set = None
        link_list_auth = None
        link_list_msc = None
        link_de_val = None

        links_display = []

        if author:
            # get all links corresponding to author input
            link_list_auth = link_helpers.get_links_from_author(author)
            link_set = link_helpers.update_set_by_intersect(
                link_set, set(link_list_auth)
            )

        if msc_val:
            # get all links corresponding to msc input
            link_list_msc = link_helpers.get_links_from_mscs(msc_val)
            link_set = link_helpers.update_set_by_intersect(
                link_set, set(link_list_msc)
            )

        if de_val:
            # get all links corresponding to document input
            link_de_val = Link.query.filter_by(
                document=de_val, matched_by="LinksApi"
            ).all()
            link_set = link_helpers.update_set_by_intersect(
                link_set, set(link_de_val)
            )

        if not (author or msc_val or de_val):
            link_set = set(Link.query.filter_by(matched_by="LinksApi").all())

        if link_set:
            links_display = [get_display(element) for element in link_set]

        return links_display


link_item_arguments = reqparse.RequestParser()

link_item_arguments.add_argument("document", type=int, required=True)

link_item_arguments.add_argument("external_id", type=str, required=True)

link_item_arguments.add_argument("partner", type=str, required=True)


@ns.route("/item/")
class LinkItem(Resource):
    @api.expect(link_item_arguments)
    @api.marshal_with(link)
    @api.doc(
        params={
            "document": {
                "description": "Ex: 3273551 (DE number, available "
                "in the bibtex of each document at "
                "https://zbmath.org/)"
            },
            "external_id": {
                "description": "Ex (DLMF): 11.14#I1.i1.p1"
                "(identifier of the link)"
            },
            "type": {"description": "Ex: DLMF, OEIS, etc."},
        }
    )
    def get(self):
        """Check relations between a given link and a given zbMATH object"""
        args = request.args
        de_val = args["document"]
        source_val = args["external_id"]
        partner_name = args["type"]

        return_link = Link.query.filter_by(
            document=de_val, external_id=source_val, type=partner_name
        ).first()

        return_display = []
        if return_link:
            return_display = get_display(return_link)

        return return_display

    @api.expect(link_item_arguments)
    @api.response(201, "Link successfully created.")
    @api.doc(
        params={
            "zbl code": {"description": "Ex: 0171.38503"},
            "source identifier": {"description": "Ex: 11.14#I1.i1.p1"},
            "partner name": {"description": "Ex: DLMF"},
        }
    )
    @token_required
    @api.doc(security="apikey")
    def post(self):
        """Create a new link related to a zbMATH object"""
        args = request.args

        zbl_val = args["zbl code"]
        source_val = args["source identifier]
        source_name = args["partner name"]
        link_date = datetime.utcnow()
        provider = helpers.get_provider()

        message_list = []

        partner = Partner.query.filter_by(name=source_name).first()
        if partner:
            partner_name = partner.name
        else:
            message_list.append("Invalid partner name")

        target_obj = ZBTarget.query.filter_by(zbl_code=zbl_val).first()
        if not target_obj:
            message_list.append("Zbl code is not in the database")

        source_obj = Source.query.filter_by(id=source_val).first()
        if not source_obj:
            message_list.append("Invalid external id")

        if len(message_list) > 0:
            return helpers.make_message(422, message_list)

        date_established = link_date
        date_added = link_date
        try:
            new_link = Link(
                document=zbl_val,
                external_id=source_val,
                type=partner_name,
                matched_by="LinksApi",
                created_by=provider,
                created_at=date_established,
                matched_at=date_added,
            )
            db.session.add(new_link)
            db.session.commit()
        except Exception as e:
            return helpers.make_message(409, str(e))

        return None, 201

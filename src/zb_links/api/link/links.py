# ------------------------------------------------------------------------------
# Link window (2 GET + 1 POST)
# ------------------------------------------------------------------------------

from datetime import datetime

from flask import request
from flask_restx import Resource, reqparse

from zb_links.api.link.display import get_display, link
from zb_links.api.link.helpers import helpers, link_helpers
from zb_links.api.restx import token_required, api
from zb_links.db.models import Link, Partner, db, ZBTarget, Source

ns = api.namespace(
    "link", description="Operations related to linking to zbMATH"
)

search_by_arguments = reqparse.RequestParser()

search_by_arguments.add_argument("author", type=str, required=False)

search_by_arguments.add_argument(
    "msc classification code", type=str, required=False
)


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
            "msc classification code": {
                "description": "Ex: 33-00 (multiple inputs with space as "
                               "delimiter) "
            },
        }
    )
    def get(self):
        """Retrieve links for given zbMATH objects"""
        args = request.args

        author = None
        msc_val = None
        if "author" in args:
            author = args["author"].lower()
        if "msc classification code" in args:
            msc_val = args["msc classification code"].lower()

        link_set = set()
        link_list_auth = None
        link_list_msc = None

        if author:
            # get all links corresponding to author input
            link_list_auth = link_helpers.get_links_from_author(author)
            link_set = set(link_list_auth)

        if msc_val:
            # get all links corresponding to msc input
            link_list_msc = link_helpers.get_links_from_mscs(msc_val)
            link_set = set(link_list_msc)

        if link_list_auth and link_list_msc:
            link_set = set.intersection(
                set(link_list_auth), set(link_list_msc)
            )

        if not (author or msc_val):
            link_set = set(Link.query.all())

        links_display = [get_display(element) for element in link_set]

        return links_display


link_item_arguments = reqparse.RequestParser()

link_item_arguments.add_argument("zbl code", type=str, required=True)

link_item_arguments.add_argument("source identifier", type=str, required=True)

link_item_arguments.add_argument("partner name", type=str, required=True)

link_create_arguments = link_item_arguments.copy()

link_create_arguments.add_argument("link relation", type=str, required=True)


@ns.route("/item/")
class LinkItem(Resource):
    @api.expect(link_item_arguments)
    @api.marshal_with(link)
    @api.doc(
        params={
            "zbl code": {"description": "Ex: 0171.38503"},
            "source identifier": {"description": "Ex: 11.14#I1.i1.p1"},
            "partner name": {"description": "Ex: DLMF"},
        }
    )
    def get(self):
        """Check relations between a given link and a given zbMATH object"""
        args = request.args
        zbl_val = args["zbl code"]
        source_val = args["source identifier"]
        partner_name = args["partner name"]

        return_link = Link.query.filter_by(
            source_identifier=source_val,
            target_id=zbl_val,
            partner_name=partner_name,
        ).first()

        return_display = []
        if return_link:
            return_display = get_display(return_link)

        return return_display

    @api.expect(link_create_arguments)
    @api.response(201, "Link successfully created.")
    @api.doc(
        params={
            "zbl code": {"description": "Ex: 0171.38503"},
            "source identifier": {"description": "Ex: 11.14#I1.i1.p1"},
            "partner name": {"description": "Ex: DLMF"},
            "link relation": {"description": "Ex: None"},
        }
    )
    @token_required
    @api.doc(security="apikey")
    def post(self):
        """Create a new link related to a zbMATH object"""
        args = request.args

        zbl_val = args["zbl code"]
        source_val = args["source identifier"]
        source_name = args["partner name"]
        link_date = datetime.utcnow()
        provider_id = 1

        message_list = []
        partner_name = None

        partner = Partner.query.filter_by(name=source_name).first()
        if partner:
            partner_id = partner.partner_id
            partner_name = partner.name
        else:
            message_list.append("Invalid partner name")
            partner_id = None

        target_obj = ZBTarget.query.filter_by(zbl_code=zbl_val).first()
        if not target_obj:
            message_list.append("Zbl code is not the database")

        source_obj = Source.query.filter_by(
            identifier=source_val, partner=partner_name
        ).first()
        if source_obj:
            source_id = source_obj.source_id
        else:
            message_list.append("Invalid source identifier")
            source_id = None

        if len(message_list) > 0:
            return helpers.make_message(422, message_list)

        number_links = Link.query.count()

        new_link_id = number_links + 1

        date_established = link_date
        date_added = link_date

        relation = "generic relation"

        try:
            new_link = Link(
                new_link_id,
                source_id,
                source_val,
                zbl_val,
                partner_id,
                partner_name,
                date_established,
                date_added,
                provider_id,
                relation,
            )
            db.session.add(new_link)
            db.session.commit()
        except Exception as e:
            return helpers.make_message(409, str(e))

        return None, 201

# ------------------------------------------------------------------------------
# Link window (2 GET + 1 POST)
# ------------------------------------------------------------------------------

from datetime import datetime

from flask import request
from flask_restx import Resource, reqparse
from werkzeug.exceptions import BadRequest

from zb_links.api.link.display import get_display, link
from zb_links.api.link.helpers import (
    helpers,
    link_helpers,
    source_helpers,
    target_helpers,
)
from zb_links.api.restx import api, token_required
from zb_links.db.models import Link, Partner, Source, ZBTarget, db

ns = api.namespace(
    "link", description="Operations related to linking to zbMATH"
)

search_by_arguments = reqparse.RequestParser()

search_by_arguments.add_argument("authors", type=str, required=False)

search_by_arguments.add_argument("MSC code", type=str, required=False)

search_by_arguments.add_argument("DE number", type=str, required=False)


@api.expect(search_by_arguments)
@ns.route("/")
class LinkCollection(Resource):
    @api.marshal_list_with(link)
    @api.doc(
        params={
            "authors": {
                "description": "Ex: Abramowitz, M. "
                "(multiple inputs with ; as delimiter)"
            },
            "DE number": {
                "description": "Ex: 3273551 (DE number)"
                " or 0171.38503 (Zbl code)"
            },
            "MSC code": {
                "description": "Ex: 33-00 "
                "(multiple inputs with space as "
                "delimiter) "
            },
        }
    )
    def get(self):
        """Retrieve links for given zbMATH objects"""
        args = request.args

        author = None
        msc_val = None
        doc_id = None
        if "authors" in args:
            author = args["authors"].lower()
        if "MSC code" in args:
            msc_val = args["MSC code"].lower()
        if "DE number" in args:
            doc_id = args["DE number"].strip()

        link_set = None
        link_list_auth = None
        link_list_msc = None
        link_doc_id = None

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

        if doc_id:
            id_type = link_helpers.get_id_type(doc_id)
            if id_type == "zbl_code":
                doc_id = target_helpers.get_de_from_zbl_id(doc_id)

            # get all links corresponding to document input
            link_doc_id = Link.query.filter_by(
                document=doc_id, matched_by="LinksApi"
            ).all()
            link_set = link_helpers.update_set_by_intersect(
                link_set, set(link_doc_id)
            )

        if not (author or msc_val or doc_id):
            link_set = set(Link.query.filter_by(matched_by="LinksApi").all())

        if link_set:
            links_display = [get_display(element) for element in link_set]

        return links_display


link_item_arguments = reqparse.RequestParser()

link_item_arguments.add_argument("DE number", type=str, required=True)

link_item_arguments.add_argument("external id", type=str, required=True)

link_item_arguments.add_argument("partner", type=str, required=True)


@ns.route("/item/")
class LinkItem(Resource):
    @api.expect(link_item_arguments)
    @api.marshal_with(link)
    @api.doc(
        params={
            "DE number": {
                "description": "Ex: 3273551 (DE number)"
                " or 0171.38503 (Zbl code)"
            },
            "external id": {
                "description": "Ex (DLMF): 11.14#I1.i1.p1"
                "(identifier of the link)"
            },
            "partner": {"description": "Ex: DLMF, OEIS, etc."},
        }
    )
    def get(self):
        """Check relations between a given link and a given zbMATH object"""
        args = request.args
        doc_id = args["DE number"].strip()
        source_val = args["external id"]
        partner_name = args["partner"]

        return_link = None
        id_type = link_helpers.get_id_type(doc_id)
        if id_type == "zbl_code":
            doc_id = target_helpers.get_de_from_zbl_id(doc_id)

        return_link = Link.query.filter_by(
            document=doc_id, external_id=source_val, type=partner_name
        ).first()

        return_display = []
        if return_link:
            return_display = get_display(return_link)

        return return_display

    @api.expect(link_item_arguments)
    @api.response(201, "Link successfully created.")
    @api.doc(
        params={
            "DE number": {
                "description": "Ex: 3273551 (DE number)"
                " or 0171.38503 (Zbl code)"
            },
            "external id": {
                "description": "Ex (DLMF): 11.14#I1.i1.p1"
                "(identifier of the link)"
            },
            "partner": {"description": "Ex: DLMF, OEIS, etc."},
        }
    )
    @token_required
    @api.doc(security="apikey")
    def post(self):
        """Create a new link related to a zbMATH object"""
        args = request.args

        doc_id = args["DE number"].strip()
        id_type = link_helpers.get_id_type(doc_id)
        if id_type == "zbl_code":
            doc_id = target_helpers.get_de_from_zbl_id(doc_id)

        source_val = args["external id"]
        source_name = args["partner"]
        title_name = None
        try:
            title_name = args["title"]
        except BadRequest:
            pass
        link_date = datetime.utcnow()
        provider = helpers.get_provider()

        message_list = []

        partner = Partner.query.filter_by(name=source_name).first()
        if partner:
            partner_name = partner.name
        else:
            message_list.append("Invalid partner name")

        target_obj = ZBTarget.query.filter_by(id=doc_id).first()
        if not target_obj:
            message_list.append("This DE is not in the database")

        if len(message_list) > 0:
            return helpers.make_message(422, message_list)

        source_obj = Source.query.filter_by(id=source_val).first()
        if not source_obj:
            response = source_helpers.create_new_source(
                source_val, source_name, title_name
            )
            if response:
                return response

        date_established = link_date
        date_added = link_date
        try:
            new_link = Link(
                document=doc_id,
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

# ------------------------------------------------------------------------------
# Link window (3 GET + 1 POST + 1 DELETE + 1 PATCH)
# ------------------------------------------------------------------------------

from datetime import datetime

import pytz
from flask import redirect, request, url_for
from flask_restx import Resource, reqparse
from werkzeug.exceptions import BadRequest

from zb_links.api.link import arg_names, descriptions
from zb_links.api.link.display import get_display, link
from zb_links.api.link.helpers import (
    helpers,
    link_helpers,
    source_helpers,
    target_helpers,
)
from zb_links.api.restx import api, token_required
from zb_links.db.models import Link, Partner, Source, ZBTarget, db

dist_name = link_helpers.dist_name
dist_version = link_helpers.dist_version

ns = api.namespace(
    "link", description="Operations related to linking to zbMATH"
)

search_by_arguments = reqparse.RequestParser()

search_by_arguments.add_argument(arg_names["auth"], type=str, required=False)

search_by_arguments.add_argument(
    arg_names["classification"], type=str, required=False
)

search_by_arguments.add_argument(arg_names["doc"], type=str, required=False)


@api.expect(search_by_arguments)
@ns.route("/")
class LinkCollection(Resource):
    @api.marshal_list_with(link)
    @api.doc(
        params={
            arg_names["auth"]: {
                "description": descriptions[arg_names["auth"]]
            },
            arg_names["doc"]: {"description": descriptions[arg_names["doc"]]},
            arg_names["classification"]: {
                "description": descriptions[arg_names["classification"]]
            },
        }
    )
    def get(self):
        """Retrieve links for given zbMATH objects"""
        args = request.args

        author = None
        msc_val = None
        doc_id = None
        if arg_names["auth"] in args:
            author = args[arg_names["auth"]].lower()
        if arg_names["classification"] in args:
            msc_val = args[arg_names["classification"]].lower()
        if arg_names["doc"] in args:
            doc_id = args[arg_names["doc"]].strip()

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
            doc_id = target_helpers.get_de_from_input(doc_id)

            # get all links corresponding to document input
            link_doc_id = Link.query.filter_by(
                document=doc_id, matched_by=dist_name
            ).all()
            link_set = link_helpers.update_set_by_intersect(
                link_set, set(link_doc_id)
            )

        if not (author or msc_val or doc_id):
            print("Links")
            from zb_links.db.models import db
            print(db)
            link_set = set(Link.query.filter_by(matched_by=dist_name).all())

        if link_set:
            links_display = [get_display(element) for element in link_set]

        return links_display


link_item_arguments = reqparse.RequestParser()

link_item_arguments.add_argument(
    arg_names["document"], type=str, required=True
)

link_item_arguments.add_argument(
    arg_names["link_ext_id"], type=str, required=True
)

link_item_arguments.add_argument(
    arg_names["link_partner"], type=str, required=True
)

link_item_arguments.add_argument(
    arg_names["link_publication_date"], type=str, required=False
)

link_edit_arguments = link_item_arguments.copy()

link_edit_arguments.add_argument(
    arg_names["edit_link_doc"], type=str, required=False
)

link_edit_arguments.add_argument(
    arg_names["edit_link_ext_id"], type=str, required=False
)

link_edit_arguments.add_argument(
    arg_names["edit_link_partner"], type=str, required=False
)

link_params = {
    arg_names["document"]: {"description": descriptions[arg_names["doc"]]},
    arg_names["link_ext_id"]: {
        "description": descriptions[arg_names["link_ext_id"]]
    },
    arg_names["link_partner"]: {
        "description": descriptions[arg_names["link_partner"]]
    },
    arg_names["link_publication_date"]: {
        "description": descriptions[arg_names["link_publication_date"]]
    },
}


@ns.route("/item/")
class LinkItem(Resource):
    @api.expect(link_item_arguments)
    @api.marshal_with(link)
    @api.doc(params=link_params)
    def get(self):
        """Check relations between a given link and a given zbMATH object"""
        args = request.args
        doc_id = args[arg_names["document"]].strip()
        source_val = args[arg_names["link_ext_id"]]
        partner_name = args[arg_names["link_partner"]].lower()

        return_link = None
        doc_id = target_helpers.get_de_from_input(doc_id)
        return_link = Link.query.filter_by(
            document=doc_id, external_id=source_val, type=partner_name
        ).first()

        return_display = []
        if return_link:
            return_display = get_display(return_link)

        return return_display

    @api.expect(link_item_arguments)
    @api.response(201, "Link successfully created.")
    @api.doc(params=link_params)
    @token_required
    @api.doc(security="apikey")
    def post(self):
        """Create a new link related to a zbMATH object"""

        mbv = dist_version

        args = request.args

        doc_id = args[arg_names["document"]].strip()
        doc_id = target_helpers.get_de_from_input(doc_id)

        source_val = args[arg_names["link_ext_id"]]
        source_name = args[arg_names["link_partner"]].lower()
        title_name = None
        try:
            title_name = args["title"]
        except BadRequest:
            pass

        try:
            mbv = args["matched_by_version"]
        except BadRequest:
            pass

        message_list = []

        date_added = None
        try:
            date_added = args[arg_names["link_publication_date"]]
        except BadRequest:
            pass
        if date_added:
            try:
                date_added = datetime.strptime(
                    args[arg_names["link_publication_date"]], "%Y-%m-%d"
                )
            except ValueError:
                message_list.append("Invalid date format")
        else:
            date_added = datetime.now(pytz.timezone("Europe/Berlin"))

        partner = Partner.query.filter_by(name=source_name).first()
        if partner:
            partner_name = partner.name
        else:
            message_list.append("Invalid partner name")

        target_obj = ZBTarget.query.filter_by(id=doc_id).first()
        if not target_obj:
            message_list.append("This DE is not in the database")

        if link_helpers.link_exists((doc_id, source_val, source_name)):
            message_list.append("This link already exists in the database")

        if len(message_list) > 0:
            return helpers.make_message(422, message_list)

        source_obj = Source.query.filter_by(
            id=source_val, partner=source_name
        ).first()
        if not source_obj:
            response = source_helpers.create_new_source(
                source_val, source_name, title_name
            )
            if response:
                return response

        try:
            new_link = Link(
                document=doc_id,
                external_id=source_val,
                type=partner_name,
                matched_by=dist_name,
                matched_by_version=mbv,
                matched_at=date_added,
            )
            db.session.add(new_link)
            db.session.commit()
        except Exception as e:
            return helpers.make_message(409, str(e))

        return None, 201

    @api.expect(link_edit_arguments)
    @api.response(204, "Link successfully edited.")
    @api.doc(params=link_params)
    @token_required
    @api.doc(security="apikey")
    def patch(self):
        """Edit a link"""
        args = request.args
        link_document = args[arg_names["document"]].strip()
        link_external_id = args[arg_names["link_ext_id"]]
        link_type = args[arg_names["link_partner"]].lower()
        title_name = None
        try:
            title_name = args["title"]
        except BadRequest:
            pass

        title_same = True

        link = None
        link_document = target_helpers.get_de_from_input(link_document)
        link = Link.query.filter_by(
            document=link_document,
            external_id=link_external_id,
            type=link_type,
        ).first()

        if not link:
            return helpers.make_message(422, "No such link")

        message_list = []
        new_doc_id = None
        new_ext_id = None
        new_partner = None
        if arg_names["edit_link_doc"] in args:
            new_doc_id = args[arg_names["edit_link_doc"]].strip()
            new_doc_id = target_helpers.get_de_from_input(new_doc_id)
            if not new_doc_id:
                message_list.append(
                    "Document with the new id is not in the database"
                )
            link_document = new_doc_id

        if arg_names["edit_link_partner"] in args:
            new_partner_name = args[arg_names["edit_link_partner"]].strip()

            new_partner = Partner.query.filter_by(
                name=new_partner_name
            ).first()
            if not new_partner:
                message_list.append("Invalid new partner name")
            link_type = new_partner_name

        if len(message_list) > 0:
            return helpers.make_message(422, message_list)

        if arg_names["edit_link_ext_id"] in args:
            new_ext_id = args[arg_names["edit_link_ext_id"]].strip()
            link_external_id = new_ext_id

        source_obj = Source.query.filter_by(
            id=link_external_id, partner=link_type
        ).first()
        if not source_obj:
            response = source_helpers.create_new_source(
                new_ext_id, link_type, title_name
            )
            if response:
                return response

        source_obj = Source.query.filter_by(
            id=link_external_id, partner=link_type
        ).first()
        if title_name:
            source_title = source_obj.title
            if title_name != source_title:
                title_same = False
                response = source_helpers.edit_source_title(
                    new_ext_id, link_type, title_name
                )
                if response:
                    return response

        if not (new_doc_id or new_ext_id or new_partner) and title_same:
            return helpers.make_message(422, "empty data for a patch")

        link_data_tuple = (link_document, link_external_id, link_type)
        if link_helpers.link_exists(link_data_tuple):
            if title_same:
                return helpers.make_message(
                    422, "This link already exists in the database"
                )
        else:
            link.document = link_document
            link.external_id = link_external_id
            link.type = link_type
            date_modified = datetime.now(pytz.timezone("Europe/Berlin"))
            link.last_modified_at = date_modified

            db.session.commit()

        return None, 204

    @api.expect(link_item_arguments)
    @api.response(204, "Link successfully deleted.")
    @api.doc(params=link_params)
    @token_required
    @api.doc(security="apikey")
    def delete(self):
        """Delete a link"""
        args = request.args
        doc_id = args[arg_names["document"]].strip()
        source_val = args[arg_names["link_ext_id"]]
        partner_name = args[arg_names["link_partner"]].lower()

        doc_id = target_helpers.get_de_from_input(doc_id)
        link_to_delete_query = Link.query.filter_by(
            document=doc_id, external_id=source_val, type=partner_name
        )

        if not link_to_delete_query.first():
            return helpers.make_message(422, "No such link")

        link_to_delete_query.delete()
        db.session.commit()

        return None, 204


@ns.route("/item/<doc_id>")
class LinkDoc(Resource):
    @api.doc(
        params={
            "doc_id": {
                "description": "Ex: 3273551 (DE number)"
                " or 0171.38503 (Zbl code)"
            }
        }
    )
    def get(self, doc_id):
        """Retrieve links for a given zbMATH object"""
        return redirect(
            url_for("links_api.link_link_collection", DE_number=doc_id)
        )

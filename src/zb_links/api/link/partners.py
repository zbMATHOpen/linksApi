# ------------------------------------------------------------------------------
# Partner window (1 GET + 1 PUT + 1 POST)
# ------------------------------------------------------------------------------

from flask import request
from flask_restx import Resource, fields, reqparse

from zb_links.api.link.helpers import helpers
from zb_links.api.restx import api, token_required
from zb_links.db.models import Partner, db

ns = api.namespace("partner", description="Linking partners of zbMATH")

partner = api.model(
    "Linking partner",
    {
        "name": fields.String(required=True, description="Partner name"),
        "display_name": fields.String(
            required=True, description="Partner name as displayed"
        ),
        "scheme": fields.String(
            required=True,
            description="Schematic followed to establish partner identifier",
        ),
        "url": fields.String(
            required=True, description="Web address of partner"
        ),
    },
)

partner_edit_arguments = reqparse.RequestParser()

partner_edit_arguments.add_argument(
    "current name", type=str, required=True
)

partner_edit_arguments.add_argument("new name", type=str)

partner_edit_arguments.add_argument("new scheme", type=str)

partner_edit_arguments.add_argument("new url", type=str)

partner_insert_arguments = reqparse.RequestParser()

partner_insert_arguments.add_argument("name", type=str, required=True)

partner_insert_arguments.add_argument("display_name", type=str, required=True)

partner_insert_arguments.add_argument("scheme", type=str, required=True)

partner_insert_arguments.add_argument("url", type=str, required=True)


@ns.route("/")
class PartnerCollection(Resource):
    @api.marshal_list_with(partner)
    def get(self):
        """Retrieve data of zbMATH partners"""
        partners = Partner.query.all()

        return partners

    @api.expect(partner_edit_arguments)
    @token_required
    @api.doc(security="apikey")
    def put(self):
        """Edit data of a zbMATH partner"""
        args = request.args
        arg_keys = args.keys()
        arg_key_list = []
        for a_key in arg_keys:
            arg_key_list.append(a_key)

        partner_name = args["current name"].lower()

        partner_query = Partner.query.filter_by(name=partner_name)
        partner_to_edit = Partner.query.get(partner_name)

        if not partner_to_edit:
            return helpers.make_message(422, "Invalid input")

        partner_name = partner_to_edit.name
        partner_display_name = partner_to_edit.display_name
        partner_scheme = partner_to_edit.scheme
        partner_url = partner_to_edit.url
        if "new name" in arg_key_list:
            partner_display_name = args["new name"]
            partner_name = partner_display_name.lower()
        if "new scheme" in arg_key_list:
            partner_scheme = args["new scheme"]
        if "new url" in arg_key_list:
            partner_url = args["new url"]

        data_to_update = dict(
            name=partner_name,
            display_name=partner_display_name,
            scheme=partner_scheme,
            url=partner_url,
        )

        partner_query.update(data_to_update)
        db.session.commit()

    @api.expect(partner_insert_arguments)
    @api.response(201, "Partner successfully created.")
    @token_required
    @api.doc(security="apikey")
    def post(self):
        """Create a new partner related to zbMATH"""
        args = request.args

        try:
            partner_exists = Partner.query.get(args["name"])

            if partner_exists:
                return helpers.make_message(
                    422, "Partner is already in the database"
                )

        except Exception as e:
            return helpers.make_message(409, str(e))

        try:
            partner = Partner(
                name=args["name"],
                display_name=args["display_name"],
                scheme=args["scheme"],
                url=args["url"],
            )

            db.session.add(partner)
            db.session.commit()
        except Exception as e:
            return helpers.make_message(409, str(e))

        return None, 201

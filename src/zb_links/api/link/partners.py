# ------------------------------------------------------------------------------
# Partner window (1 GET + 1 PUT)
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
    "current partner name", type=str, required=True
)

partner_edit_arguments.add_argument("new partner name", type=str)

partner_edit_arguments.add_argument("partner id scheme", type=str)

partner_edit_arguments.add_argument("partner url", type=str)


@ns.route("/")
class PartnerCollection(Resource):
    @api.marshal_list_with(partner)
    def get(self):
        """Retrieve data of a zbMATH partner (partner id, name, scheme, url)"""
        partners = Partner.query.all()

        return partners

    @api.expect(partner_edit_arguments)
    @token_required
    @api.doc(security="apikey")
    def put(self):
        """Edit data of a zbMATH partner (partner id, name, scheme, url)"""
        args = request.args
        arg_keys = args.keys()
        arg_key_list = []
        for a_key in arg_keys:
            arg_key_list.append(a_key)

        partner_name = args["current partner name"].lower()

        partner_query = Partner.query.filter_by(name=partner_name)
        partner_to_edit = Partner.query.get(partner_name)

        if not partner_to_edit:
            return helpers.make_message(422, "Invalid input")

        partner_name = partner_to_edit.name
        partner_display_name = partner_to_edit.display_name
        partner_scheme = partner_to_edit.scheme
        partner_url = partner_to_edit.url
        if "new partner name" in arg_key_list:
            partner_display_name = args["new partner name"]
            partner_name = partner_display_name.lower()
        if "partner id scheme" in arg_key_list:
            partner_scheme = args["partner id scheme"]
        if "partner url" in arg_key_list:
            partner_url = args["partner url"]

        data_to_update = dict(
            name=partner_name,
            display_name=partner_display_name,
            scheme=partner_scheme,
            url=partner_url
        )

        partner_query.update(data_to_update)
        db.session.commit()

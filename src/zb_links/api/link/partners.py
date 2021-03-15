# ------------------------------------------------------------------------------
# Partner window (1 GET)
# ------------------------------------------------------------------------------

from flask import request
from flask_restx import Resource, fields,  reqparse
from zb_links.db.models import db, Partner
from zb_links.api.restx import api, token_required
from zb_links.api.link.helpers import helpers

ns = api.namespace(
    "partner",
    description="Linking partners of zbMATH"
)

partner = api.model(
    "Linking partner", {
        "partner_id": fields.Integer(
            readOnly=True,
            description="The unique identifier of a zbMATH partner"
        ),
        "name": fields.String(
            required=True,
            description="Partner name"
        ),
        "scheme": fields.String(
            required=True,
            description="Schematic followed to establish partner identifier"
        ),
        "url": fields.String(
            required=True,
            description="Web address of partner"
        )
    }
)

partner_edit_arguments = reqparse.RequestParser()

partner_edit_arguments.add_argument("partner id", type=int, required=True)

partner_edit_arguments.add_argument("partner name", type=str)

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
    @api.doc(security='apikey')
    def put(self):
        """Edit data of a zbMATH partner (partner id, name, scheme, url)"""
        args = request.args
        arg_keys = args.keys()
        arg_key_list = []
        for a_key in arg_keys:
            arg_key_list.append(a_key)

        partner_id = args["partner id"]

        partner_query = Partner.query.filter_by(partner_id=partner_id)
        partner_to_edit = Partner.query.get(partner_id)
        if not partner_to_edit:
            return helpers.make_message(422, "Invalid input")

        partner_name = partner_to_edit.name
        partner_scheme = partner_to_edit.scheme
        partner_url = partner_to_edit.url
        if "partner name" in arg_key_list:
            partner_name = args["partner name"]
        if "partner id scheme" in arg_key_list:
            partner_scheme = args["partner id scheme"]
        if "partner url" in arg_key_list:
            partner_url = args["partner url"]

        data_to_update = dict(
            name=partner_name,
            scheme=partner_scheme,
            url=partner_url
        )

        partner_query.update(data_to_update)
        db.session.commit()

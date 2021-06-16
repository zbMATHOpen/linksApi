# ------------------------------------------------------------------------------
# Source window (1 GET)
# ------------------------------------------------------------------------------

from flask_restx import Resource, reqparse
from flask import request
from zb_links.api.restx import api
from zb_links.db.models import Source

ns = api.namespace("source", description="url of links in the source")

url_arguments = reqparse.RequestParser()

url_arguments.add_argument("partner", type=str, required=True)


@ns.route("/")
class SourceCollection(Resource):
    @api.expect(url_arguments)
    @api.doc(
        params={
            "partner": {"description": "Ex: DLMF, OEIS, etc."},
        }
    )
    def get(self):
        """List of links in the source"""
        args = request.args
        partner_name = args["partner"]

        sources = Source.query.filter(Source.partner == partner_name).all()
        display_list = []
        for a_source in sources:
            if a_source.id not in display_list:
                display_list.append(a_source.url)
        return display_list

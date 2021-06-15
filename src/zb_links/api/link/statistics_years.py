# ------------------------------------------------------------------------------
# Statistics years of publication window (1 GET)
# ------------------------------------------------------------------------------

from collections import Counter

from flask import request
from flask_restx import Resource, reqparse

from zb_links.api.restx import api
from zb_links.db.models import Link, ZBTarget

ns = api.namespace("statistics")

year_arguments = reqparse.RequestParser()

year_arguments.add_argument("type", type=str, required=True)


@ns.route("/years/")
class YearCollection(Resource):
    @api.expect(year_arguments)
    @api.doc(
        params={
            "type": {"description": "Ex: DLMF, OEIS, etc."},
        }
    )
    def get(self):
        """Occurrence of years of publication of papers"""
        args = request.args
        partner_name = args["type"]

        queries = (
            ZBTarget.query.join(Link, Link.document == ZBTarget.id)
            .filter(Link.type == partner_name)
            .all()
        )

        years_list = [str(item.year) for item in queries]
        counter = Counter(years_list).most_common()
        return counter

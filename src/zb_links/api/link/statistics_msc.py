# ------------------------------------------------------------------------------
# Statistics MSC window (1 GET)
# ------------------------------------------------------------------------------

from collections import Counter
from flask import request
from flask_restx import Resource, reqparse

from zb_links.api.restx import api
from zb_links.db.models import ZBTarget, Link

ns = api.namespace(
    "statistics",
    description="Distribution of primary MSC codes and years of publication "
    "of referenced papers for a given partner",
)

msc_arguments = reqparse.RequestParser()

msc_arguments.add_argument("type", type=str, required=True)


@ns.route("/msc/")
class MSCCollection(Resource):
    @api.expect(msc_arguments)
    @api.doc(
        params={
            "type": {"description": "Ex: DLMF, OEIS, etc."},
        }
    )
    def get(self):
        """Occurrence of primary 2-digit level MSC codes"""
        args = request.args
        partner_name = args["type"]

        queries = (ZBTarget.query.join(Link, Link.document == ZBTarget.id)
            .filter(Link.type == partner_name)
            .all()
        )

        msc_primary_list = [
            str(item.classification)[0:2]
            for item in queries
            if item.classification
        ]
        counter = Counter(msc_primary_list).most_common()
        return counter

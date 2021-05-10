# ------------------------------------------------------------------------------
# Statistics MSC window (1 GET)
# ------------------------------------------------------------------------------

from collections import Counter
from flask import request
from zb_links.api.link.display import get_display, link
from flask_restx import Resource, reqparse

from zb_links.api.restx import api
from zb_links.db.models import ZBTarget, Link

ns = api.namespace(
    "statistics",
    description="Distribution of primary MSC codes and years of publication "
    "of referenced papers in the source",
)

msc_arguments = reqparse.RequestParser()

msc_arguments.add_argument("partner name", type=str, required=True)


# Distribution of MSC codes
# @ns.route("/msc/")
# class MSCCollection(Resource):
#     @staticmethod
#     def get():
#         """Occurrence of primary 2-digit level MSC codes"""
#         queries = ZBTarget.query.\
#             join(Link, Link.document == ZBTarget.id).\
#             filter(Link.type == "DLMF").all()
#         msc_primary_list = [
#             str(item.classification)[0:2]
#             for item in queries
#             if item.classification]
#         counter = Counter(msc_primary_list).most_common()
#         return counter

@ns.route("/msc/")
class MSCCollection(Resource):
    @api.expect(msc_arguments)
    @api.marshal_with(link)
    @api.doc(
        params={
            "partner name": {"description": "Ex: DLMF"},
        }
    )
    def get(self):
        """Occurrence of primary 2-digit level MSC codes"""
        args = request.args
        partner_name = args["type"]

        queries = ZBTarget.query.\
            join(Link, Link.document == ZBTarget.id).\
            filter_by(partner_name=partner_name).\
            all()

        msc_primary_list = [
            str(item.classification)[0:2]
            for item in queries
            if item.classification]
        counter = Counter(msc_primary_list).most_common()
        return counter

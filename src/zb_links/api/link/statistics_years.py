# ------------------------------------------------------------------------------
# Statistics years of publication window (1 GET)
# ------------------------------------------------------------------------------

from collections import Counter

from flask_restx import Resource

from zb_links.api.restx import api
from zb_links.db.models import ZBTarget, Link

ns = api.namespace("statistics")


# Distribution of years of publication
@ns.route("/years/")
class YearCollection(Resource):
    @staticmethod
    def get():
        """Occurrence of years of publication of papers"""
        queries = ZBTarget.query.\
            join(Link, Link.document == ZBTarget.id).\
            filter(Link.type == "DLMF").all()
        years_list = [str(item.year) for item in queries]
        counter = Counter(years_list).most_common()
        return counter

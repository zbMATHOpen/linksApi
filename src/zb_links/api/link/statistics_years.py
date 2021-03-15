# ------------------------------------------------------------------------------
# Statistics years of publication window (1 GET)
# ------------------------------------------------------------------------------

from flask_restx import Resource
from zb_links.api.restx import api
from zb_links.db.models import ZBTarget
from collections import Counter

ns = api.namespace("statistics")


# Distribution of years of publication
@ns.route("/years/")
class YearCollection(Resource):

    def get(self):
        """Occurrence of years of publication of papers"""
        queries = ZBTarget.query.all()
        years_list = [
            str(item.publication_date)
            for item in queries
        ]
        counter = Counter(years_list).most_common()
        return counter

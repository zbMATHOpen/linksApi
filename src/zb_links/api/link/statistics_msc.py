# ------------------------------------------------------------------------------
# Statistics MSC window (1 GET)
# ------------------------------------------------------------------------------

from collections import Counter

from flask_restx import Resource

from zb_links.api.restx import api
from zb_links.db.models import ZBTarget

ns = api.namespace(
    "statistics",
    description="Distribution of primary MSC codes and years of publication "
    "of referenced papers in the source",
)


# Distribution of MSC codes
@ns.route("/msc/")
class MSCCollection(Resource):
    @staticmethod
    def get():
        """Occurrence of primary 2-digit level MSC codes"""
        queries = ZBTarget.query.all()
        msc_primary_list = [str(item.msc)[0:2] for item in queries if item.msc]
        counter = Counter(msc_primary_list).most_common()
        return counter

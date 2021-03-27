# ------------------------------------------------------------------------------
# Source window (1 GET)
# ------------------------------------------------------------------------------

from flask_restx import Resource

from zb_links.api.restx import api
from zb_links.db.models import Source

ns = api.namespace("source", description="url of links in the source")


# List of link sources (list of all DLMF backlinks)
@ns.route("/")
class SourceCollection(Resource):
    @staticmethod
    def get():
        """List of all links in the source"""
        sources = Source.query.all()
        display_list = []
        for a_source in sources:
            if a_source.identifier not in display_list:
                display_list.append(a_source.url)
        return display_list

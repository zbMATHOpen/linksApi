from flask import Blueprint

from zb_links.db.models import db


viewbp = Blueprint("view", __name__)


@viewbp.cli.command("add")
def add_schemas():

    connection = db.engine.connect()
    view_request = """
        CREATE OR REPLACE VIEW author_groups AS
        SELECT deid.document, a_id.name
        FROM document_external_ids AS deid
    	INNER JOIN math_author_ids AS a_id
    	INNER JOIN math_author_ids AS a_id2
    	ON a_id.author = a_id2.author
    	ON deid.document = a_id2.document
        WHERE deid.matched_by = 'LinksApi';
    """
    connection.execute(view_request)

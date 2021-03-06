from zb_links.db.models import db


def add_view():

    connection = db.engine.connect()
    view_request = """
        CREATE OR REPLACE VIEW author_groups AS
        SELECT deid.document, a_id.name
        FROM document_external_ids AS deid
        INNER JOIN math_author_ids AS a_id
        INNER JOIN math_author_ids AS a_id2
        ON a_id.author = a_id2.author
        ON deid.document = a_id2.document
        WHERE deid.matched_by = 'zbmath-links-api';
    """
    connection.execute(view_request)

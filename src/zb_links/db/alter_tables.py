from flask import Blueprint

from zb_links.db.models import db


alterbp = Blueprint("alter", __name__)


def get_max_external_id():

    connection = db.engine.connect()

    max_request = "SELECT MAX(id) FROM document_external_ids;"
    max_id_tuple = connection.execute(max_request).fetchall()[0]
    if not max_id_tuple[0]:
        return 1

    return max_id_tuple[0]


@alterbp.cli.command("tables")
def alter_tables():

    connection = db.engine.connect()

    sequence_request = "CREATE SEQUENCE IF NOT EXISTS external_id_seq;"
    connection.execute(sequence_request)

    alter_val_request = """
        ALTER TABLE document_external_ids
        ALTER COLUMN id
        SET DEFAULT nextval('external_id_seq');
    """
    connection.execute(alter_val_request)

    alter_request = (
        "ALTER SEQUENCE external_id_seq OWNED BY document_external_ids.id;"
    )
    connection.execute(alter_request)

    max_id = get_max_external_id()
    set_value_request = f"SELECT setval('external_id_seq', {max_id});"
    connection.execute(set_value_request)

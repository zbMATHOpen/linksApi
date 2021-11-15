from zb_links.db.models import db


def add_tables():

    connection = db.engine.connect()
    create_author_id_table = """
    CREATE TABLE IF NOT EXISTS math_author_ids(
       id INT PRIMARY KEY      NOT NULL,
       name VARCHAR ( 255 ),
       document INT,
       author INT
    );
    """
    connection.execute(create_author_id_table)

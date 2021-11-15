#!/bin/bash
flask db init
flask schema_add
flask db migrate
flask db upgrade
flask extra_tables_add
flask view_add
flask seed_all

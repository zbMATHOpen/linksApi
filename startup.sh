#!/bin/bash
flask db init
flask schema add
flask db migrate
flask db upgrade
flask extra_tables add
flask view add
flask seed all

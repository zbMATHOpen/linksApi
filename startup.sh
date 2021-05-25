#!/bin/bash
flask manage_db drop_all
flask db init
flask schema add
flask db migrate
flask db upgrade
flask seed all

#!/bin/bash
flask manage_db reset
flask db init
flask db migrate
flask db upgrade
flask seed all

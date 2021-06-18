# flake8: noqa
import os

from cherrytrack.config.logging import *

###
# General config
###
LOCALHOST = os.environ.get("LOCALHOST", "127.0.0.1")

###
# Database config
###
DATABASE_SERVER_HOST = f"{LOCALHOST}"
DATABASE_SERVER_PORT = 3306
DATABASE_NAME = "psd_cherrytrack_dev"
DATABASE_USERNAME = "root"
DATABASE_PASSWORD = ""

###
# flask-sqlalchemy config
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/
# This URI needs to be overridden whenever one of the database config (above) changes
###
SQLALCHEMY_DATABASE_URI = (
    f"{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_SERVER_HOST}:{DATABASE_SERVER_PORT}/{DATABASE_NAME}"
)

# hide deprecation warning
SQLALCHEMY_TRACK_MODIFICATIONS = False

RO_CONN_STRING = f"{DATABASE_USERNAME}@{LOCALHOST}"
AUTOMATION_SYSTEM_RUNS_TABLE = "automation_system_runs"
AUTOMATION_SYSTEMS_TABLE = "automation_systems"
SOURCE_PLATE_WELLS_TABLE = "source_plate_wells"
DESTINATION_PLATE_WELLS_TABLE = "destination_plate_wells"

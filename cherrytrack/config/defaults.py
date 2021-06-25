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
SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_SERVER_HOST}:{DATABASE_SERVER_PORT}/{DATABASE_NAME}"

# hide deprecation warning
SQLALCHEMY_TRACK_MODIFICATIONS = False

RO_CONN_STRING = f"{DATABASE_USERNAME}@{LOCALHOST}"
TABLE_AUTOMATION_SYSTEM_RUNS = "automation_system_runs"
TABLE_AUTOMATION_SYSTEMS = "automation_systems"
TABLE_SOURCE_PLATE_WELLS = "source_plate_wells"
TABLE_DESTINATION_PLATE_WELLS = "destination_plate_wells"
TABLE_CONTROL_PLATE_WELLS = "control_plate_wells"

# flake8: noqa
from cherrytrack.config.defaults import *

# setting here will overwrite those in 'defaults.py'

###
# Flask config
###
TESTING = True

###
# Database config
###
DATABASE_NAME = "psd_cherrytrack_test"

###
# flask-sqlalchemy config
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/
# This URI needs to be overridden whenever one of the database config (above) changes
###
SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_SERVER_HOST}:{DATABASE_SERVER_PORT}/{DATABASE_NAME}"

###
# logging config
###
LOGGING["loggers"]["cherrytrack"]["level"] = "DEBUG"
LOGGING["loggers"]["cherrytrack"]["handlers"] = ["colored_stream_dev"]

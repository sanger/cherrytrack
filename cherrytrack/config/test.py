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
# logging config
###
LOGGING["loggers"]["cherrytrack"]["level"] = "DEBUG"
LOGGING["loggers"]["cherrytrack"]["handlers"] = ["colored_stream_dev"]

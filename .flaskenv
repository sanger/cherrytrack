# use publicly acessible env variables in this file
#   https://flask.palletsprojects.com/en/2.0.x/cli//#environment-variables-from-dotenv

# https://flask.palletsprojects.com/en/2.0.x/cli//#application-discovery
FLASK_APP=cherrytrack

# https://flask.palletsprojects.com/en/2.0.x/cli//#setting-command-options
FLASK_RUN_HOST=0.0.0.0
FLASK_RUN_PORT=8000

# https://flask.palletsprojects.com/en/2.0.x/config/#environment-and-debug-features
FLASK_ENV=development

# path to the settings file which Flask will use
SETTINGS_PATH=config/development.py

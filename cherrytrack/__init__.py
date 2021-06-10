import logging
import logging.config
from http import HTTPStatus

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from cherrytrack.config.logging import LOGGING

logger = logging.getLogger(__name__)

db = SQLAlchemy()
migrate = Migrate()


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    if test_config is None:
        # load the config, if it exists, when not testing
        app.config.from_envvar("SETTINGS_PATH")
    else:
        # currently testing using the "SETTINGS_PATH" env var but leaving this for potential use
        # load the test config if passed in
        app.config.from_mapping(test_config)

    logging.config.dictConfig(LOGGING)

    # import the models here so that flask_migrate knows about them
    import cherrytrack.models  # noqa

    migrate.init_app(app, db)

    from cherrytrack.blueprints import plates, runs

    app.register_blueprint(plates.bp)
    app.register_blueprint(runs.bp)

    @app.get("/health")
    def health_check():
        return "Factory working", HTTPStatus.OK

    return app

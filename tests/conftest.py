import os

import pytest

from cherrytrack import create_app


@pytest.fixture
def app():
    # set the 'SETTINGS_PATH' env variable to easily switch to the testing environment when creating an app
    os.environ["SETTINGS_PATH"] = "config/test.py"

    app = create_app()

    yield app


@pytest.fixture
def client(app):
    return app.test_client()

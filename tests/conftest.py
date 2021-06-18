import os
import pytest
from cherrytrack import create_app
from cherrytrack.helpers.mysql import create_mysql_connection_engine, get_table
from cherrytrack.models import AutomationSystemRun, SourcePlateWell
from sqlalchemy import select
from sqlalchemy.sql import text
from tests.fixtures.data.runs import RUNS
from tests.fixtures.data.source_plates import SOURCE_PLATES


@pytest.fixture
def app():
    # set the 'SETTINGS_PATH' env variable to easily switch to the testing environment when creating an app
    os.environ["SETTINGS_PATH"] = "config/test.py"

    app = create_app()

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def sql_engine(app):
    return create_mysql_connection_engine(app.config["RO_CONN_STRING"], app.config["DATABASE_NAME"])


@pytest.fixture
def runs(app, sql_engine):
    try:
        table = get_table(sql_engine, app.config["AUTOMATION_SYSTEM_RUNS_TABLE"])

        def delete_data():
            with sql_engine.begin() as connection:
                connection.execute(table.delete())
                connection.execute(text(f"ALTER TABLE {app.config['AUTOMATION_SYSTEM_RUNS_TABLE']} AUTO_INCREMENT = 1"))

        delete_data()  # delete all rows from table first

        inserted_data = []
        with sql_engine.begin() as connection:
            print("Inserting test data")
            connection.execute(table.insert(), RUNS)

            stmt = select(AutomationSystemRun)
            inserted_data = connection.execute(stmt)

        #  yield the inserted data
        yield inserted_data.all()

    finally:  # clear up after the fixture is used
        delete_data()

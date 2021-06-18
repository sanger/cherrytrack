import os
import pytest
from cherrytrack import create_app
from cherrytrack.helpers.mysql import create_mysql_connection_engine, get_table
from cherrytrack.models import AutomationSystemRun, SourcePlateWell, DestinationPlateWell
from sqlalchemy import select
from sqlalchemy.sql import text
from tests.fixtures.data.runs import RUNS
from tests.fixtures.data.source_plate_wells import SOURCE_PLATE_WELLS
from tests.fixtures.data.destination_plate_wells import DESTINATION_PLATE_WELLS


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
        table_name = app.config["AUTOMATION_SYSTEM_RUNS_TABLE"]
        delete_data(sql_engine, table_name)

        inserted_data = []
        with sql_engine.begin() as connection:
            print("Inserting test data")
            table = get_table(sql_engine, table_name)
            connection.execute(table.insert(), RUNS)

            stmt = select(AutomationSystemRun)
            inserted_data = connection.execute(stmt)

        #  yield the inserted data
        yield inserted_data.all()

    finally:  # clear up after the fixture is used
        delete_data(sql_engine, table_name)


@pytest.fixture
def source_plate_wells(app, sql_engine):
    try:
        table_name = app.config["SOURCE_PLATE_WELLS_TABLE"]
        delete_data(sql_engine, table_name)  # delete all rows from table first

        inserted_data = []
        with sql_engine.begin() as connection:
            print("Inserting test data")
            table = get_table(sql_engine, table_name)
            connection.execute(table.insert(), SOURCE_PLATE_WELLS)

            stmt = select(SourcePlateWell)
            inserted_data = connection.execute(stmt)

        #  yield the inserted data
        yield inserted_data.all()

    finally:  # clear up after the fixture is used
        delete_data(sql_engine, table_name)


@pytest.fixture
def destination_plate_wells(app, sql_engine):
    try:
        table_name = app.config["DESTINATION_PLATE_WELLS_TABLE"]
        delete_data(sql_engine, table_name)  # delete all rows from table first

        inserted_data = []
        with sql_engine.begin() as connection:
            print("Inserting test data")
            table = get_table(sql_engine, table_name)
            connection.execute(table.insert(), DESTINATION_PLATE_WELLS)

            stmt = select(DestinationPlateWell)
            inserted_data = connection.execute(stmt)

        #  yield the inserted data
        yield inserted_data.all()

    finally:  # clear up after the fixture is used
        delete_data(sql_engine, table_name)


def delete_data(sql_engine, table_name):
    table = get_table(sql_engine, table_name)

    with sql_engine.begin() as connection:
        connection.execute(table.delete())
        connection.execute(text(f"ALTER TABLE {table_name} AUTO_INCREMENT = 1"))

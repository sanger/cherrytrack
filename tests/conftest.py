import os
import pytest
from cherrytrack import db, create_app

from cherrytrack.models import (
    AutomationSystemRun,
    AutomationSystem,
    SourcePlateWell,
    DestinationPlateWell,
    ControlPlateWell,
)

ControlPlateWell
from sqlalchemy.sql import text
from tests.fixtures.data.runs import RUNS
from tests.fixtures.data.source_plate_wells import SOURCE_PLATE_WELLS
from tests.fixtures.data.destination_plate_wells import DESTINATION_PLATE_WELLS
from tests.fixtures.data.control_plate_well import CONTROL_PLATE_WELLS
from tests.fixtures.data.automation_systems import AUTOMATION_SYSTEMS


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
def automation_systems(app):
    with app.app_context():
        try:
            for system in AUTOMATION_SYSTEMS:
                db.session.add(AutomationSystem(**system))
            db.session.commit()

            #  yield the inserted data
            yield AutomationSystem.query.all()

        finally:
            delete_data(AutomationSystem, app.config["TABLE_AUTOMATION_SYSTEMS"])


@pytest.fixture
def runs(app):
    with app.app_context():
        try:
            for run in RUNS:
                db.session.add(AutomationSystemRun(**run))
            db.session.commit()

            #  yield the inserted data
            yield AutomationSystemRun.query.all()

        finally:
            delete_data(AutomationSystemRun, app.config["TABLE_AUTOMATION_SYSTEM_RUNS"])


@pytest.fixture
def source_plate_wells(app):
    with app.app_context():
        try:
            for spw in SOURCE_PLATE_WELLS:
                db.session.add(SourcePlateWell(**spw))
            db.session.commit()

            #  yield the inserted data
            yield SourcePlateWell.query.all()

        finally:
            delete_data(SourcePlateWell, app.config["TABLE_SOURCE_PLATE_WELLS"])


@pytest.fixture
def control_plate_wells(app):
    with app.app_context():
        try:
            for cpw in CONTROL_PLATE_WELLS:
                db.session.add(ControlPlateWell(**cpw))
            db.session.commit()

            #  yield the inserted data
            yield ControlPlateWell.query.all()

        finally:
            delete_data(ControlPlateWell, app.config["TABLE_CONTROL_PLATE_WELLS"])


@pytest.fixture
def destination_plate_wells(app):
    with app.app_context():
        try:
            for dpw in DESTINATION_PLATE_WELLS:
                db.session.add(DestinationPlateWell(**dpw))
            db.session.commit()

            #  yield the inserted data
            yield DestinationPlateWell.query.all()

        finally:
            delete_data(DestinationPlateWell, app.config["TABLE_DESTINATION_PLATE_WELLS"])


# clear up after the fixture is used - remove data rows and reset primary key
def delete_data(model, table_name):
    model.query.delete()
    db.session.commit()
    sql = text(f"ALTER TABLE {table_name} AUTO_INCREMENT = 1")
    db.engine.execute(sql)

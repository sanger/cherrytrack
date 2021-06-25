from cherrytrack.helpers.runs import get_run_info, get_automation_system_for_id, get_automation_system_run_for_id
from pytest import raises


def test_get_run_info(app, client, automation_systems, runs):
    with app.app_context():
        run = runs[0]
        actual = get_run_info(run.id)

        expected = {
            "id": run.id,
            "user_id": run.user_id,
            "liquid_handler_serial_number": "LHS000001",
            "automation_system_name": "CPA",
            "automation_system_manufacturer": "biosero",
        }
        assert actual == expected


def test_get_run_info_failed(app, client):
    with app.app_context():
        exception = ""
        with raises(Exception) as e:
            exception = e
            get_run_info(1)

        assert "Failed to find a automation system run with id 1" == str(exception.value)


def test_get_automation_system_run_for_id(app, client, automation_systems, runs):
    with app.app_context():
        run = runs[0]
        actual = get_automation_system_run_for_id(run.id)
        assert actual == run


def test_get_automation_system_run_for_id_failed(app, client):
    with app.app_context():
        exception = ""
        with raises(Exception) as e:
            exception = e
            get_automation_system_run_for_id(1)

        assert "Failed to find a automation system run with id 1" == str(exception.value)


def test_get_automation_system_for_id(app, client, automation_systems):
    with app.app_context():
        automation_system = automation_systems[0]
        actual = get_automation_system_for_id(automation_system.id)
        assert actual == automation_system


def test_get_automation_system_for_id_failed(app):
    with app.app_context():
        exception = ""
        with raises(Exception) as e:
            exception = e
            get_automation_system_for_id(1)
        assert "Failed to find a automation system with id 1" == str(exception.value)

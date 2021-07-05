from http import HTTPStatus
from unittest.mock import patch


def test_get_automation_system_runs_endpoint_successful(app, client):
    with app.app_context():
        run_info = {
            "id": 1,
            "user_id": "ab1",
            "automation_system_name": "CPA",
            "automation_system_manufacturer": "biosero",
            "liquid_handler_serial_number": "LHS000001",
        }

        with patch("cherrytrack.blueprints.runs.get_run_info", return_value=run_info):

            response = client.get("/automation-system-runs/1")

            assert response.status_code == HTTPStatus.OK

            assert response.json == {"data": run_info}


def test_get_automation_system_runs_endpoint_get_run_info_fails(app, client):
    with app.app_context():
        with patch("cherrytrack.blueprints.runs.get_run_info", side_effect=Exception()):

            response = client.get("/automation-system-runs/1")

            assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR

            assert response.json == {"errors": ["Failed to get automation system run info: "]}


def test_get_automation_system_runs_endpoint_unknown_run_id(app, client):
    with app.app_context():
        run_id = 0
        response = client.get(f"/automation-system-runs/{run_id}")

        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
        assert response.json == {
            "errors": [
                f"Failed to get automation system run info: Failed to find a automation system run with id {run_id}"
            ]
        }


def test_get_automation_system_runs_endpoint_no_run_id(app, client):
    with app.app_context():
        response = client.get("/automation-system-runs")

        assert response.status_code == HTTPStatus.NOT_FOUND


def test_get_automation_system_runs_endpoint_with_non_int_run_id(app, client):
    with app.app_context():
        response = client.get("/automation-system-runs/xxx")

        assert response.status_code == HTTPStatus.NOT_FOUND

from http import HTTPStatus


def test_get_automation_system_run(app, client):
    with app.app_context():
        run_id = 1
        response = client.get(f"/automation-system-runs/{run_id}")

        assert response.status_code == HTTPStatus.OK
        assert response.json == {"data": {"id": run_id, "liquid_handler_serial_number": "LHS000001", "user_id": "ab12"}}


def test_get_automation_system_run_no_run_for_run_id(app, client):
    with app.app_context():
        run_id = 0
        response = client.get(f"/automation-system-runs/{run_id}")

        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
        assert response.json == {"errors": ["Failed to get automation system run info for the given run id"]}


def test_get_automation_system_run_no_run_id(app, client):
    with app.app_context():
        response = client.get("/automation-system-runs")

        assert response.status_code == HTTPStatus.NOT_FOUND

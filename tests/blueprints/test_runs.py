from http import HTTPStatus


def test_get_automation_system_run(app, client):
    with app.app_context():
        response = client.get("/automation-system-runs/1")

        assert response.status_code == HTTPStatus.OK

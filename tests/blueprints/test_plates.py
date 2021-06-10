from http import HTTPStatus


def test_get_source_plates(app, client):
    with app.app_context():
        response = client.get("/source-plates")

        assert response.status_code == HTTPStatus.OK

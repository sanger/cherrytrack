from http import HTTPStatus
from unittest.mock import patch


def test_get_source_plates_endpoint_successful(
    app,
    client,
    automation_systems,
    runs,
    source_plate_wells,
    control_plate_wells,
    destination_plate_wells,
):
    with app.app_context():
        source_plate = source_plate_wells[0]
        response = client.get(f"/source-plates/{source_plate.barcode}")

        assert response.status_code == HTTPStatus.OK
        assert len(response.json["data"]["samples"]) == 3
        assert response.json["data"]["barcode"] == source_plate.barcode


def test_get_source_plates_endpoint_successful_fails(app, client):
    with app.app_context():
        with patch("cherrytrack.blueprints.plates.get_samples_for_source_plate", side_effect=Exception()):

            response = client.get("/source-plates/anUnknownBarcode")

            assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR

            assert response.json == {"errors": ["Failed to get source plate info: "]}


def test_get_source_plates_endpoint_unknown_source_barcode(app, client):
    with app.app_context():
        source_barcode = "anUnknownBarcode"
        response = client.get(f"/source-plates/{source_barcode}")
        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR


def test_get_source_plates_endpoint_no_source_barcode(app, client):
    with app.app_context():
        response = client.get("/source-plates")

        assert response.status_code == HTTPStatus.NOT_FOUND


def test_get_destination_plates_endpoint_successful(
    app,
    client,
    automation_systems,
    runs,
    source_plate_wells,
    control_plate_wells,
    destination_plate_wells,
):
    with app.app_context():
        destination_plate = destination_plate_wells[0]
        response = client.get(f"/destination-plates/{destination_plate.barcode}")

        assert response.status_code == HTTPStatus.OK
        assert len(response.json["data"]["wells"]) == 5

        assert response.json["data"]["barcode"] == destination_plate.barcode
        assert response.json["data"]["wells"][0]["type"] == "sample"
        assert response.json["data"]["wells"][1]["type"] == "sample"
        assert response.json["data"]["wells"][2]["type"] == "sample"
        assert response.json["data"]["wells"][3]["type"] == "control"
        assert response.json["data"]["wells"][4]["type"] == "empty"


def test_get_destination_plates_endpoint_fails(app, client):
    with app.app_context():
        with patch("cherrytrack.blueprints.plates.get_wells_for_destination_plate", side_effect=Exception()):

            response = client.get("/destination-plates/anUnknownBarcode")

            assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR

            assert response.json == {"errors": ["Failed to get destination plate info: "]}


def test_get_destination_plates_endpoint_unknown_destination_barcode(app, client):
    with app.app_context():
        destination_barcode = "anUnknownBarcode"
        response = client.get(f"/destination-plates/{destination_barcode}")
        assert response.json == {
            "errors": [
                "Failed to get destination plate info: Failed to find wells for destination plate barcode anUnknownBarcode"
            ]
        }

        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR


def test_get_destination_plates_endpoint_no_destination_barcode(app, client):
    with app.app_context():
        response = client.get("/destination-plates")

        assert response.status_code == HTTPStatus.NOT_FOUND

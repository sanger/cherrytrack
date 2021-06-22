from http import HTTPStatus
from unittest.mock import patch


def test_get_source_plates_endpoint_successful(
    app,
    client,
    automation_systems,
    runs,
    source_plate_wells,
    destination_plate_wells,
):
    with app.app_context():
        source_plate = source_plate_wells[0]
        response = client.get(f"/source-plates/{source_plate['barcode']}")

        assert response.status_code == HTTPStatus.OK
        assert len(response.json["data"]["samples"]) == 3
        assert response.json["data"]["barcode"] == source_plate.barcode
        assert response.json["data"]["barcode"] == source_plate.barcode
        assert response.json["data"]["samples"][0]["source_plate_well_id"] == source_plate.id
        assert response.json["data"]["samples"][0]["source_barcode"] == source_plate.barcode
        assert response.json["data"]["samples"][0]["source_coordinate"] == source_plate.coordinate
        assert response.json["data"]["samples"][0]["sample_id"] == source_plate.sample_id
        assert response.json["data"]["samples"][0]["rna_id"] == source_plate.rna_id
        assert response.json["data"]["samples"][0]["lab_id"] == source_plate.lab_id
        assert response.json["data"]["samples"][0]["destination_plate_well_id"] == "1"
        assert response.json["data"]["samples"][0]["destination_barcode"] == "DS000010021"
        assert response.json["data"]["samples"][0]["destination_coordinate"] == "A2"
        assert response.json["data"]["samples"][0]["automation_system_run_id"] == "1"
        assert response.json["data"]["samples"][0]["picked"] is True
        assert response.json["data"]["samples"][1]["destination_plate_well_id"] == "3"
        assert response.json["data"]["samples"][1]["destination_barcode"] == "DS000010021"
        assert response.json["data"]["samples"][1]["destination_coordinate"] == "C4"
        assert response.json["data"]["samples"][1]["automation_system_run_id"] == "1"
        assert response.json["data"]["samples"][1]["picked"] is True
        assert response.json["data"]["samples"][2]["destination_plate_well_id"] == ""
        assert response.json["data"]["samples"][2]["destination_barcode"] == ""
        assert response.json["data"]["samples"][2]["destination_coordinate"] == ""
        assert response.json["data"]["samples"][2]["automation_system_run_id"] == ""
        assert response.json["data"]["samples"][2]["picked"] is False


def test_get_source_plates_endpoint_successful_fails(app, client):
    with app.app_context():
        with patch("cherrytrack.blueprints.plates.get_samples_for_source_plate", side_effect=Exception()):

            response = client.get("/source-plates/aUnknownBarcode")

            assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR

            assert response.json == {"errors": ["Failed to get samples for the given source plate barcode."]}


def test_get_source_plates_endpoint_unknown_source_barcode(app, client):
    with app.app_context():
        source_barcode = "aUnknownBarcode"
        response = client.get(f"/source-plates/{source_barcode}")
        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR


def test_get_source_plates_endpoint_no_source_barcode(app, client):
    with app.app_context():
        response = client.get("/source-plates")

        assert response.status_code == HTTPStatus.NOT_FOUND

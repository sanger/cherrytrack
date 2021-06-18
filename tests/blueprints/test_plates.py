from http import HTTPStatus


def test_get_source_plates(
    app,
    client,
    runs,
    source_plate_wells,
    destination_plate_wells,
):
    with app.app_context():
        source_plate = source_plate_wells[0]
        response = client.get(f"/source-plates/{source_plate['barcode']}")

        assert response.status_code == HTTPStatus.OK
        assert len(response.json["data"]) == 4
        assert response.json["data"][0]["source_plate_well_id"] == source_plate.id
        assert response.json["data"][0]["source_barcode"] == source_plate.barcode
        assert response.json["data"][0]["source_coordinate"] == source_plate.coordinate
        assert response.json["data"][0]["sample_id"] == source_plate.sample_id
        assert response.json["data"][0]["rna_id"] == source_plate.rna_id
        assert response.json["data"][0]["lab_id"] == source_plate.lab_id
        assert response.json["data"][0]["destination_plate_well_id"] == "1"
        assert response.json["data"][0]["destination_barcode"] == "DS000010021"
        assert response.json["data"][0]["destination_coordinate"] == "A2"
        assert response.json["data"][0]["automation_system_run_id"] != ""
        assert response.json["data"][0]["picked"] is True
        assert response.json["data"][1]["automation_system_run_id"] != ""
        assert response.json["data"][1]["picked"] is True
        assert response.json["data"][2]["automation_system_run_id"] != ""
        assert response.json["data"][2]["picked"] is True
        assert response.json["data"][3]["automation_system_run_id"] == ""
        assert response.json["data"][3]["picked"] is False


def test_get_source_plates_unknown_source_barcode(app, client):
    with app.app_context():
        source_barcode = "aUnknownBarcode"
        response = client.get(f"/source-plates/{source_barcode}")
        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR

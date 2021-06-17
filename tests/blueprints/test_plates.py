from http import HTTPStatus


def test_get_source_plates(app, client):
    with app.app_context():
        source_barcode = "DS000030001"
        response = client.get(f"/source-plates/{source_barcode}")
        assert response.status_code == HTTPStatus.OK
        assert len(response.json["data"]) == 76
        assert response.json["data"][0]["source_barcode"] == source_barcode
        assert response.json["data"][1]["source_barcode"] == source_barcode
        assert response.json["data"][0]["sample_id"]
        assert response.json["data"][0]["rna_id"]
        assert response.json["data"][0]["lab_id"]
        assert response.json["data"][0]["source_plate_well_id"]
        assert response.json["data"][0]["source_barcode"]
        assert response.json["data"][0]["source_coordinate"]
        assert response.json["data"][0]["destination_plate_well_id"] == ""
        assert response.json["data"][0]["destination_barcode"] == ""
        assert response.json["data"][0]["destination_coordinate"] == ""
        assert response.json["data"][0]["automation_system_run_id"] == ""
        assert response.json["data"][0]["picked"] is False


def test_get_source_plates_unknown_source_barcode(app, client):
    with app.app_context():
        source_barcode = "aUnknownBarcode"
        response = client.get(f"/source-plates/{source_barcode}")
        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR

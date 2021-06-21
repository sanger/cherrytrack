from cherrytrack.helpers.plates import get_samples_for_source_plate
from pytest import raises


def test_get_samples_for_source_plate_successful(
    app,
    automation_systems,
    runs,
    source_plate_wells,
    destination_plate_wells,
):
    with app.app_context():
        source_plate_barcode = source_plate_wells[0].barcode
        result = get_samples_for_source_plate(source_plate_barcode)

        expected_result = [
            {
                "source_plate_well_id": 1,
                "source_barcode": "DS000010001",
                "source_coordinate": "A2",
                "sample_id": "487e1b70-ad22-4716-a913-1001bc89d559",
                "lab_id": "MK",
                "rna_id": "RNA-S-00001-00000008",
                "destination_plate_well_id": "1",
                "destination_barcode": "DS000010021",
                "destination_coordinate": "A2",
                "automation_system_run_id": "1",
                "picked": True,
            },
            {
                "source_plate_well_id": 3,
                "source_barcode": "DS000010001",
                "source_coordinate": "A5",
                "sample_id": "499324b8-e4cc-4baf-a1a5-86a3a449b573",
                "lab_id": "MK",
                "rna_id": "RNA-S-00001-00000001",
                "destination_plate_well_id": "3",
                "destination_barcode": "DS000010021",
                "destination_coordinate": "C4",
                "automation_system_run_id": "1",
                "picked": True,
            },
            {
                "source_plate_well_id": 4,
                "source_barcode": "DS000010001",
                "source_coordinate": "B2",
                "sample_id": "c068cfea-02be-4aec-a50d-631abcd34573",
                "lab_id": "MK",
                "rna_id": "RNA-S-00001-00000009",
                "destination_plate_well_id": "",
                "destination_barcode": "",
                "destination_coordinate": "",
                "automation_system_run_id": "",
                "picked": False,
            },
        ]
        assert result == expected_result


def test_get_samples_for_source_plate_failed(app):
    with app.app_context():
        exception = ""
        with raises(Exception) as e:
            exception = e
            get_samples_for_source_plate("aUnknownBarcode")

        assert "Failed to find samples for source plate barcode aUnknownBarcode" == str(exception.value)

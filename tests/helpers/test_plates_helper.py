from pytest import raises

from cherrytrack.helpers.plates import get_samples_for_source_plate, get_wells_for_destination_plate


def test_get_samples_for_source_plate_successful(
    app,
    automation_systems,
    runs,
    source_plate_wells,
    control_plate_wells,
    destination_plate_wells,
):
    with app.app_context():
        source_plate_barcode = source_plate_wells[0].barcode
        timestamp = source_plate_wells[0].created_at
        actual = get_samples_for_source_plate(source_plate_barcode)

        expected = [
            {
                "automation_system_run_id": 1,
                "picked": True,
                "destination_barcode": "DS000010021",
                "destination_coordinate": "A2",
                "type": "sample",
                "source_barcode": "DS000010001",
                "source_coordinate": "C3",
                "rna_id": "RNA-S-00001-00000008",
                "lab_id": "MK",
                "lh_sample_uuid": "487e1b70-ad22-4716-a913-1001bc89d559",
                "created_at": timestamp,
                "date_picked": timestamp,
            },
            {
                "automation_system_run_id": 1,
                "picked": True,
                "destination_barcode": "DS000010021",
                "destination_coordinate": "C4",
                "type": "sample",
                "source_barcode": "DS000010001",
                "source_coordinate": "A5",
                "rna_id": "RNA-S-00001-00000001",
                "lab_id": "MK",
                "lh_sample_uuid": "499324b8-e4cc-4baf-a1a5-86a3a449b573",
                "created_at": timestamp,
                "date_picked": timestamp,
            },
            {
                "automation_system_run_id": "",
                "picked": False,
                "destination_barcode": "",
                "destination_coordinate": "",
                "type": "sample",
                "source_barcode": "DS000010001",
                "source_coordinate": "B2",
                "rna_id": "RNA-S-00001-00000009",
                "lab_id": "MK",
                "lh_sample_uuid": "c068cfea-02be-4aec-a50d-631abcd34573",
                "created_at": timestamp,
                "date_picked": "",
            },
        ]

        for sample in actual:
            assert sample in expected


def test_get_samples_for_source_plate_failed(app):
    with app.app_context():
        with raises(Exception) as e:
            get_samples_for_source_plate("anUnknownBarcode")
            assert "Failed to find samples for source plate barcode anUnknownBarcode" == str(e.value)


def test_get_wells_for_destination_plate_successful(
    app,
    automation_systems,
    runs,
    source_plate_wells,
    control_plate_wells,
    destination_plate_wells,
):
    with app.app_context():
        destination_plate_barcode = destination_plate_wells[0].barcode
        timestamp = destination_plate_wells[0].created_at
        actual = get_wells_for_destination_plate(destination_plate_barcode)

        expected = [
            {
                "automation_system_run_id": 1,
                "destination_coordinate": "A2",
                "type": "sample",
                "source_barcode": "DS000010001",
                "source_coordinate": "C3",
                "rna_id": "RNA-S-00001-00000008",
                "lab_id": "MK",
                "lh_sample_uuid": "487e1b70-ad22-4716-a913-1001bc89d559",
                "picked": True,
                "created_at": timestamp,
                "date_picked": timestamp,
            },
            {
                "automation_system_run_id": 1,
                "destination_coordinate": "B2",
                "type": "sample",
                "source_barcode": "DS000010002",
                "source_coordinate": "A3",
                "rna_id": "RNA-S-00001-00000004",
                "lab_id": "MK",
                "lh_sample_uuid": "6254c4c9-73ad-42e3-9926-af329f8a090f",
                "picked": True,
                "created_at": timestamp,
                "date_picked": timestamp,
            },
            {
                "automation_system_run_id": 1,
                "destination_coordinate": "C4",
                "type": "sample",
                "source_barcode": "DS000010001",
                "source_coordinate": "A5",
                "rna_id": "RNA-S-00001-00000001",
                "lab_id": "MK",
                "lh_sample_uuid": "499324b8-e4cc-4baf-a1a5-86a3a449b573",
                "picked": True,
                "created_at": timestamp,
                "date_picked": timestamp,
            },
            {
                "automation_system_run_id": 1,
                "destination_coordinate": "A1",
                "type": "control",
                "control_barcode": "DS000010012",
                "control_coordinate": "B7",
                "control": "positive",
                "picked": True,
                "created_at": timestamp,
                "date_picked": timestamp,
            },
            {
                "automation_system_run_id": 1,
                "destination_coordinate": "E3",
                "type": "empty",
                "picked": False,
                "created_at": timestamp,
                "date_picked": "",
            },
        ]

        for sample in actual:
            assert sample in expected


def test_get_wells_for_destination_plate_failed(app):
    with app.app_context():
        with raises(Exception) as e:
            get_wells_for_destination_plate("anUnknownBarcode")
            assert "Failed to find wells for destination plate barcode anUnknownBarcode" == str(e.value)

import logging
from typing import Dict, List, Union

from cherrytrack import db
from cherrytrack.models import ControlPlateWell, DestinationPlateWell, SourcePlateWell

logger = logging.getLogger(__name__)


def get_samples_for_source_plate(source_barcode: str) -> List[Dict[str, Union[bool, str]]]:
    logger.info("Attempting to get samples from source_plate_wells with the source barcode")

    query_results = (
        db.session.query(
            SourcePlateWell.id.label("source_plate_well_id"),
            SourcePlateWell.barcode.label("source_barcode"),
            SourcePlateWell.coordinate.label("source_coordinate"),
            SourcePlateWell.sample_id,
            SourcePlateWell.rna_id,
            SourcePlateWell.lab_id,
            DestinationPlateWell.automation_system_run_id,
            DestinationPlateWell.id.label("destination_plate_well_id"),
            DestinationPlateWell.barcode.label("destination_barcode"),
            DestinationPlateWell.coordinate.label("destination_coordinate"),
        )
        .filter(SourcePlateWell.barcode == source_barcode)
        .outerjoin(DestinationPlateWell, SourcePlateWell.id == DestinationPlateWell.source_plate_well_id)
        .all()
    )

    if len(query_results) == 0:
        raise Exception(f"Failed to find samples for source plate barcode {source_barcode}")

    samples = []
    for row in query_results:
        samples.append(
            {
                "picked": bool(row.automation_system_run_id),
                "automation_system_run_id": row.automation_system_run_id or "",
                "destination_barcode": row.destination_barcode or "",
                "destination_coordinate": row.destination_coordinate or "",
                **get_well_content(row),
            }
        )

    return samples


def get_wells_for_destination_plate(destination_barcode: str) -> List[Dict[str, Union[bool, str]]]:
    logger.info("Attempting to get samples from destination_plate_wells with the destination barcode")

    query_results = (
        db.session.query(
            DestinationPlateWell.automation_system_run_id,
            DestinationPlateWell.id.label("destination_plate_well_id"),
            DestinationPlateWell.barcode.label("destination_barcode"),
            DestinationPlateWell.coordinate.label("destination_coordinate"),
            SourcePlateWell.id.label("source_plate_well_id"),
            SourcePlateWell.barcode.label("source_barcode"),
            SourcePlateWell.coordinate.label("source_coordinate"),
            SourcePlateWell.sample_id,
            SourcePlateWell.rna_id,
            SourcePlateWell.lab_id,
            ControlPlateWell.id.label("control_plate_well_id"),
            ControlPlateWell.barcode.label("control_barcode"),
            ControlPlateWell.coordinate.label("control_coordinate"),
            ControlPlateWell.control,
        )
        .filter(DestinationPlateWell.barcode == destination_barcode)
        .outerjoin(SourcePlateWell, DestinationPlateWell.source_plate_well_id == SourcePlateWell.id)
        .outerjoin(ControlPlateWell, DestinationPlateWell.control_plate_well_id == ControlPlateWell.id)
        .all()
    )

    if len(query_results) == 0:
        raise Exception(f"Failed to find wells for destination plate barcode {destination_barcode}")

    samples = []
    for row in query_results:
        samples.append(
            {
                "automation_system_run_id": row.automation_system_run_id,
                "destination_coordinate": row.destination_coordinate,
                **get_well_content(row),
            }
        )

    return samples


def get_well_content(row):
    if row.source_plate_well_id:
        return {
            "type": "sample",
            "source_barcode": row.source_barcode,
            "source_coordinate": row.source_coordinate,
            "rna_id": row.rna_id,
            "lab_id": row.lab_id,
            "lh_sample_uuid": row.sample_id,
        }
    elif getattr(row, "control_plate_well_id", ""):
        return {
            "type": "control",
            "control_barcode": row.control_barcode,
            "control_coordinate": row.control_coordinate,
            "control": row.control,
        }
    else:
        return {"type": "empty"}

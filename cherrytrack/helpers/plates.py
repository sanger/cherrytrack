from cherrytrack.models import SourcePlateWell, DestinationPlateWell
import logging

from cherrytrack import db

logger = logging.getLogger(__name__)


def get_samples_for_source_plate(source_barcode):
    logger.info("Attempting to get samples from source_plate_wells with the source barcode")

    q = (
        db.session.query(SourcePlateWell, DestinationPlateWell)
        .filter(SourcePlateWell.barcode == source_barcode)
        .outerjoin(DestinationPlateWell, SourcePlateWell.id == DestinationPlateWell.source_plate_well_id)
        .all()
    )

    if len(q) == 0:
        raise Exception(f"Failed to find samples for source plate barcode {source_barcode}")

    samples = []
    for source_plate_well, destination_plate_well in q:

        samples.append(
            {
                "sample_id": source_plate_well.sample_id,
                "rna_id": source_plate_well.rna_id,
                "lab_id": source_plate_well.lab_id,
                "source_plate_well_id": source_plate_well.id,
                "source_barcode": source_plate_well.barcode,
                "source_coordinate": source_plate_well.coordinate,
                "destination_plate_well_id": getattr(destination_plate_well, "id", ""),
                "destination_barcode": getattr(destination_plate_well, "barcode", ""),
                "destination_coordinate": getattr(destination_plate_well, "coordinate", ""),
                "automation_system_run_id": getattr(destination_plate_well, "automation_system_run_id", ""),
                "picked": bool(getattr(destination_plate_well, "automation_system_run_id", "")),
            }
        )
    return samples


def get_wells_for_destination_plate(destination_barcode):
    logger.info("Attempting to get samples from source_plate_wells with the source barcode")

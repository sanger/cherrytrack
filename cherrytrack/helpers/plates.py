from cherrytrack.helpers.mysql import create_mysql_connection_engine
from flask import current_app as app
from sqlalchemy import select, and_

from cherrytrack.models import SourcePlateWell, DestinationPlateWell
import logging


logger = logging.getLogger(__name__)


def get_samples_for_source_plate(source_barcode):
    logger.info("Attempting to get samples from source_plate_wells with the source barcode")

    # assign db_connection to avoid UnboundLocalError in 'finally' block, in case of exception
    db_connection = None

    try:
        sql_engine = create_mysql_connection_engine(app.config["RO_CONN_STRING"], app.config["DATABASE_NAME"])

        stmt = (
            select(
                SourcePlateWell.sample_id,
                SourcePlateWell.rna_id,
                SourcePlateWell.lab_id,
                SourcePlateWell.id.label("source_plate_well_id"),
                SourcePlateWell.barcode.label("source_barcode"),
                SourcePlateWell.coordinate.label("source_coordinate"),
                DestinationPlateWell.id.label("destination_plate_well_id"),
                DestinationPlateWell.barcode.label("destination_barcode"),
                DestinationPlateWell.coordinate.label("destination_coordinate"),
                DestinationPlateWell.automation_system_run_id,
            )
            .outerjoin(DestinationPlateWell, SourcePlateWell.id == DestinationPlateWell.source_plate_well_id)
            .where(and_(SourcePlateWell.barcode == source_barcode))
        )

        db_connection = sql_engine.connect()
        results = db_connection.execute(stmt)

        rows_matched = results.rowcount

        if rows_matched == 0:
            raise Exception(f"Failed to find samples for source plate barcode {source_barcode}")

        samples = []
        for row in results:
            samples.append(
                {
                    "sample_id": row.sample_id,
                    "rna_id": row.rna_id,
                    "lab_id": row.lab_id,
                    "source_plate_well_id": row.source_plate_well_id,
                    "source_barcode": row.source_barcode,
                    "source_coordinate": row.source_coordinate,
                    "destination_plate_well_id": str(row.destination_plate_well_id or ""),
                    "destination_barcode": str(row.destination_barcode or ""),
                    "destination_coordinate": str(row.destination_coordinate or ""),
                    "automation_system_run_id": str(row.automation_system_run_id or ""),
                    "picked": bool(row.automation_system_run_id),
                }
            )

        return samples
    except Exception as e:
        logger.error(e)
        raise
    finally:
        if db_connection is not None:
            db_connection.close()

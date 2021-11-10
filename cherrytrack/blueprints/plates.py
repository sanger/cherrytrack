import logging

from flask import Blueprint
from flask_cors import CORS
from cherrytrack.constants import ERROR_GET_SAMPLES_FOR_DESTINATION_PLATES, ERROR_GET_SAMPLES_FOR_SOURCE_PLATES
from cherrytrack.helpers.plates import get_samples_for_source_plate, get_wells_for_destination_plate
from cherrytrack.responses import internal_server_error, ok
from cherrytrack.types import FlaskResponse

logger = logging.getLogger(__name__)

bp = Blueprint("plates", __name__)
cors = CORS(bp)


@bp.get("/destination-plates/<string:barcode>")
def get_destination_plates(barcode: str) -> FlaskResponse:
    logger.debug("Getting destination plate info...")

    try:
        # change samples to wells in Postman
        response = {"barcode": barcode, "wells": get_wells_for_destination_plate(barcode)}
        return ok(data=response)
    except Exception as e:
        logger.exception(e)

        return internal_server_error(f"{ERROR_GET_SAMPLES_FOR_DESTINATION_PLATES} {e}")


@bp.get("/source-plates/<string:barcode>")
def get_source_plates(barcode: str) -> FlaskResponse:
    logger.debug("Getting source plate info...")

    try:
        response = {"barcode": barcode, "samples": get_samples_for_source_plate(barcode)}
        return ok(data=response)
    except Exception as e:
        logger.exception(e)

        return internal_server_error(f"{ERROR_GET_SAMPLES_FOR_SOURCE_PLATES} {e}")

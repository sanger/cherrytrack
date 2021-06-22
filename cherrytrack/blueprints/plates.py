import logging

from flask import Blueprint

from cherrytrack.responses import ok, internal_server_error
from cherrytrack.types import FlaskResponse

from cherrytrack.constants import ERROR_GET_SAMPLES_FOR_SOURCE_PLATES, ERROR_GET_SAMPLES_FOR_DESTINATION_PLATES

from cherrytrack.helpers.plates import get_samples_for_source_plate, get_wells_for_destination_plate

logger = logging.getLogger(__name__)

bp = Blueprint("plates", __name__)


@bp.get("/destination-plates/<string:barcode>")
def get_destination_plates(barcode: str) -> FlaskResponse:
    logger.debug("Getting destination plate info...")

    try:
        response = {"barcode": barcode, "wells": get_wells_for_destination_plate(barcode)}
        return ok(data=response)
    except Exception as e:
        logger.exception(e)

        return internal_server_error(ERROR_GET_SAMPLES_FOR_DESTINATION_PLATES)


@bp.get("/source-plates/<string:barcode>")
def get_source_plates(barcode: str) -> FlaskResponse:
    logger.debug("Getting source plate info...")

    try:
        response = {"barcode": barcode, "samples": get_samples_for_source_plate(barcode)}
        return ok(data=response)
    except Exception as e:
        logger.exception(e)

        return internal_server_error(ERROR_GET_SAMPLES_FOR_SOURCE_PLATES)

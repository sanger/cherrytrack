import logging

from flask import Blueprint

from cherrytrack.responses import ok, internal_server_error
from cherrytrack.types import FlaskResponse

from cherrytrack.constants import ERROR_GET_SAMPLES_FOR_SOURCE_PLATES

from cherrytrack.helpers.plates import get_samples_for_source_plate

logger = logging.getLogger(__name__)

bp = Blueprint("plates", __name__)


@bp.get("/destination-plates")
def get_destination_plates() -> FlaskResponse:
    logger.debug("Getting destination plate info...")
    return ok()


@bp.get("/source-plates/<string:barcode>")
def get_source_plates(barcode: str) -> FlaskResponse:
    logger.debug("Getting source plate info...")

    try:
        return ok(data=get_samples_for_source_plate(barcode))
    except Exception as e:
        logger.exception(e)

        return internal_server_error(ERROR_GET_SAMPLES_FOR_SOURCE_PLATES)

import logging

from flask import Blueprint

from cherrytrack.responses import ok
from cherrytrack.types import FlaskResponse

logger = logging.getLogger(__name__)

bp = Blueprint("plates", __name__)


@bp.get("/destination-plates")
def get_destination_plates() -> FlaskResponse:
    logger.debug("Getting destination plate info...")
    return ok()


@bp.get("/source-plates")
def get_source_plates() -> FlaskResponse:
    logger.debug("Getting source plate info...")
    return ok()

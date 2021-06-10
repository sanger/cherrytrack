import logging

from flask import Blueprint

from cherrytrack.responses import ok
from cherrytrack.types import FlaskResponse

logger = logging.getLogger(__name__)

bp = Blueprint("runs", __name__)


@bp.get("/automation-system-runs")
def get_automation_system_runs() -> FlaskResponse:
    logger.debug("Getting automation system run info...")
    return ok()

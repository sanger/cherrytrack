import logging

from flask import Blueprint, request

from cherrytrack.responses import ok
from cherrytrack.types import FlaskResponse

logger = logging.getLogger(__name__)

bp = Blueprint("runs", __name__)


@bp.get("/automation-system-runs/<string:id>")
def get_automation_system_runs(id) -> FlaskResponse:
    logger.debug("Getting automation system run info...")

    return ok(data=get_run_info(id))

def get_run_info(id):
  # TODO: get this from the DB
  return {'id': id, 'user_id': 'ab1', 'liquid_handler_serial_number': 'aLiquidHandlerSerialNumber'}
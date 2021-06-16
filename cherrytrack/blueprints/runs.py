import logging

from flask import Blueprint
from cherrytrack.responses import ok, internal_server_error
from cherrytrack.types import FlaskResponse
from cherrytrack.constants import ERROR_GET_AUTOMATION_SYSTEM_RUN_INFO
from cherrytrack.helpers.runs import get_run_info

logger = logging.getLogger(__name__)

bp = Blueprint("runs", __name__)


@bp.get("/automation-system-runs/<string:id>")
def get_automation_system_runs(id: int) -> FlaskResponse:
    logger.debug("Getting automation system run info...")
    try:
        return ok(data=get_run_info(id))
    except Exception as e:
        logger.exception(e)

        return internal_server_error(ERROR_GET_AUTOMATION_SYSTEM_RUN_INFO)

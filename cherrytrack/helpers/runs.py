import logging
from typing import Dict, Union

from cherrytrack.models import AutomationSystem, AutomationSystemRun

logger = logging.getLogger(__name__)


def get_run_info(id: int) -> Dict[str, Union[int, str]]:
    run = get_automation_system_run_for_id(id)
    automation_system = get_automation_system_for_id(run.automation_system_id)

    return {
        "id": run.id,
        "user_id": run.user_id,
        "liquid_handler_serial_number": automation_system.liquid_handler_serial_number,
        "automation_system_name": automation_system.automation_system_name,
        "automation_system_manufacturer": automation_system.automation_system_manufacturer,
    }


def get_automation_system_run_for_id(id: int) -> AutomationSystemRun:
    automation_system_run: AutomationSystemRun = AutomationSystemRun.query.filter_by(id=id).first()

    if automation_system_run is None:
        raise Exception(f"Failed to find a automation system run with id {id}")

    return automation_system_run


def get_automation_system_for_id(id: int) -> AutomationSystem:
    automation_system: AutomationSystem = AutomationSystem.query.filter_by(id=id).first()
    # TODO: below maybe not needed as foreign key constraint would prevent run from being created if no automation
    #   system exists?
    if automation_system is None:
        raise Exception(f"Failed to find a automation system with id {id}")

    return automation_system

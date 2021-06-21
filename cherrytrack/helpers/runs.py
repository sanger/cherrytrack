from cherrytrack.helpers.mysql import create_mysql_connection_engine
from flask import current_app as app
from sqlalchemy import select
from cherrytrack.models import AutomationSystemRun, AutomationSystem
import logging

logger = logging.getLogger(__name__)


def get_run_info(id):
    run = get_automation_system_run_for_id(id)

    automation_system = get_automation_system_for_id(run.automation_system_id)

    return {
        "id": run.id,
        "user_id": run.user_id,
        "liquid_handler_serial_number": automation_system.liquid_handler_serial_number,
    }


def get_automation_system_run_for_id(id):
    # assign db_connection to avoid UnboundLocalError in 'finally' block, in case of exception
    db_connection = None

    try:
        sql_engine = create_mysql_connection_engine(app.config["RO_CONN_STRING"], app.config["DATABASE_NAME"])

        stmt = select(AutomationSystemRun).where(AutomationSystemRun.id == id)

        db_connection = sql_engine.connect()

        results = db_connection.execute(stmt)
        rows_matched = results.rowcount
        if rows_matched != 1:
            raise Exception(f"Failed to find a automation system run with id {id}")
        return results.all()[0]
    except Exception as e:
        logger.error(e)
        raise
    finally:
        if db_connection is not None:
            db_connection.close()


def get_automation_system_for_id(id):
    # assign db_connection to avoid UnboundLocalError in 'finally' block, in case of exception
    db_connection = None

    try:
        sql_engine = create_mysql_connection_engine(app.config["RO_CONN_STRING"], app.config["DATABASE_NAME"])

        stmt = select(AutomationSystem).where(AutomationSystem.id == id)

        db_connection = sql_engine.connect()

        results = db_connection.execute(stmt)
        rows_matched = results.rowcount
        if rows_matched != 1:
            raise Exception(f"Failed to find a automation system with id {id}")
        return results.all()[0]
    except Exception as e:
        logger.error(e)
        raise
    finally:
        if db_connection is not None:
            db_connection.close()

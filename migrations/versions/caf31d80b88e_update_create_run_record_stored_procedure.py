"""empty message

Revision ID: caf31d80b88e
Revises: 997dcbb7b16e
Create Date: 2021-08-13 11:17:09.793241

"""

import sqlalchemy as sa
from alembic import op
from flask import current_app
from sqlalchemy.sql import text


# revision identifiers, used by Alembic.
revision = "caf31d80b88e"
down_revision = "997dcbb7b16e"
branch_labels = None
depends_on = None


def drop_stored_procedure(procedure_name: str) -> None:
    if procedure_name is None or not procedure_name:
        raise Exception("Stored procedure name required to drop")

    op.execute(f"DROP PROCEDURE IF EXISTS `{procedure_name}`;")


def upgrade():
    db_username = current_app.config["DATABASE_USERNAME"]

    # https://stackoverflow.com/a/23206636
    conn = op.get_bind()

    drop_stored_procedure("createRunRecord")

    conn.execute(
        text(
            """
            CREATE DEFINER=:db_username@`%` PROCEDURE `createRunRecord`(
                IN input_automation_system_name VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
                IN input_gbg_method_name VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
                IN input_user_id VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
                OUT output_automation_system_run_id INT
            )
            BEGIN
            -- Rollback if there is any error
            DECLARE EXIT HANDLER FOR SQLEXCEPTION
                BEGIN
                SHOW ERRORS;
                ROLLBACK;
                END;

            -- Start of any writing operations
            START TRANSACTION;

            -- Fetch configuration for this automation system
            SET @configuration_for_system = (
                SELECT JSON_ARRAYAGG(
                    JSON_OBJECT(
                        'config_key', config_key,
                        'config_value', config_value
                    )
                )
                FROM configurations
                INNER JOIN automation_systems
                ON automation_systems.id = configurations.automation_system_id
                WHERE automation_systems.automation_system_name = input_automation_system_name
            );

            -- Close off any outstanding runs for this system to handle case of failed run
            -- where the run state was not updated from 'started'
            UPDATE `automation_system_runs` asr
            SET
                asr.end_time = now(),
                asr.state = 'aborted',
                asr.updated_at = now()
            WHERE
                asr.state = 'started'
                AND asr.automation_system_id = (
                    SELECT asys.id
                    FROM automation_systems asys
                    WHERE asys.automation_system_name = input_automation_system_name
                )
            ;

            -- Insert a new run record
            INSERT INTO `automation_system_runs` (
                automation_system_id,
                method,
                user_id,
                start_time,
                state,
                created_at,
                updated_at
            )
            VALUES (
                (
                    SELECT id FROM `automation_systems`
                    WHERE automation_system_name = input_automation_system_name
                ),
                input_gbg_method_name,
                input_user_id,
                now(),
                'started',
                now(),
                now()
            );

            -- Feth the id of the run row just created
            SELECT LAST_INSERT_ID() INTO output_automation_system_run_id;

            -- Insert the run configuration
            INSERT INTO `run_configurations` (
                automation_system_run_id,
                configuration_used,
                created_at,
                updated_at
            )
            VALUES (
                output_automation_system_run_id,
                @configuration_for_system,
                now(),
                now()
            );

            -- Finish the transaction
            COMMIT;
            END
            """
        ),
        {"db_username": db_username},
    )


def downgrade():
    db_username = current_app.config["DATABASE_USERNAME"]

    # https://stackoverflow.com/a/23206636
    conn = op.get_bind()

    drop_stored_procedure("createRunRecord")

    conn.execute(
        text(
            """
            CREATE DEFINER=:db_username@`%` PROCEDURE `createRunRecord`(
                IN input_automation_system_name VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
                IN input_gbg_method_name VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
                IN input_user_id VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
                OUT output_automation_system_run_id INT
            )
            BEGIN
            -- Rollback if there is any error
            DECLARE EXIT HANDLER FOR SQLEXCEPTION
                BEGIN
                SHOW ERRORS;
                ROLLBACK;
                END;

            -- Start of any writing operations
            START TRANSACTION;

            SET @configuration_for_system = (
                SELECT JSON_ARRAYAGG(
                    JSON_OBJECT(
                        'config_key', config_key,
                        'config_value', config_value
                    )
                )
                FROM configurations
                INNER JOIN automation_systems
                ON automation_systems.id = configurations.automation_system_id
                WHERE automation_systems.automation_system_name = input_automation_system_name
            );

            INSERT INTO `automation_system_runs` (
                automation_system_id,
                method,
                user_id,
                start_time,
                state,
                created_at,
                updated_at
            )
            VALUES (
                (
                    SELECT id FROM `automation_systems`
                    WHERE automation_system_name = input_automation_system_name
                ),
                input_gbg_method_name,
                input_user_id,
                now(),
                'started',
                now(),
                now()
            );

            SELECT LAST_INSERT_ID() INTO output_automation_system_run_id;

            INSERT INTO `run_configurations` (
                automation_system_run_id,
                configuration_used,
                created_at,
                updated_at
            )
            VALUES (
                output_automation_system_run_id,
                @configuration_for_system,
                now(),
                now()
            );

            -- Finish the transaction
            COMMIT;
            END
            """
        ),
        {"db_username": db_username},
    )

"""Create Stored Procedures

Revision ID: 06836ff03683
Revises: ee5b3041115e
Create Date: 2021-07-01 16:27:37.257131

"""
import sqlalchemy as sa
from alembic import op
from flask import current_app
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision = "06836ff03683"
down_revision = "ee5b3041115e"
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

    # createControlPlateWellsRecord
    conn.execute(
        text(
            """
            CREATE DEFINER=:db_username@`%` PROCEDURE `createControlPlateWellsRecord`(
            IN input_automation_system_run_id INT,
            IN input_barcode VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
            IN input_coordinate VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
            IN input_control VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci
            )
            BEGIN
            INSERT INTO `control_plate_wells` (
                automation_system_run_id,
                barcode,
                coordinate,
                control,
                created_at,
                updated_at
            )
            VALUES (
                input_automation_system_run_id,
                input_barcode,
                input_coordinate,
                input_control,
                now(),
                now()
            );

            END
            """
        ),
        {"db_username": db_username},
    )

    # createEmptyDestinationPlateWellsRecord
    conn.execute(
        text(
            """
            CREATE DEFINER=:db_username@`%` PROCEDURE `createEmptyDestinationPlateWellsRecord`(
            IN input_automation_system_run_id INT,
            IN input_barcode VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
            IN input_coordinate VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci

            )
            BEGIN
            INSERT INTO `destination_plate_wells` (
                automation_system_run_id,
                barcode,
                coordinate,
                source_plate_well_id,
                control_plate_well_id,
                created_at,
                updated_at
            )
            VALUES (
                input_automation_system_run_id,
                input_barcode,
                input_coordinate,
                NULL,
                NULL,
                now(),
                now()
            );

            END
            """
        ),
        {"db_username": db_username},
    )

    # createRunEventRecord
    conn.execute(
        text(
            """
            CREATE DEFINER=:db_username@`%` PROCEDURE `createRunEventRecord`(
            IN input_automation_system_run_id INT,
            IN input_type ENUM('info','warning','error'),
            IN input_event JSON
            )
            BEGIN
            INSERT INTO `run_events` (
                automation_system_run_id,
                type,
                event,
                created_at,
                updated_at
            )
            VALUES (
                input_automation_system_run_id,
                input_type,
                input_event,
                now(),
                now()
            );
            END
            """
        ),
        {"db_username": db_username},
    )

    # createRunRecord
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

    # createSourcePlateWellRecord
    conn.execute(
        text(
            """
            CREATE DEFINER=:db_username@`%` PROCEDURE `createSourcePlateWellRecord`(
            IN input_barcode VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
            IN input_coordinate VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
            IN input_sample_id VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
            IN input_rna_id VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
            IN input_lab_id VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci
            )
            BEGIN
            INSERT INTO `source_plate_wells` (
                `barcode`,
                `coordinate`,
                `sample_id`,
                `rna_id`,
                `lab_id`,
                `created_at`,
                `updated_at`
            )
            VALUES (
                input_barcode,
                input_coordinate,
                input_sample_id,
                input_rna_id,
                input_lab_id,
                now(),
                now()
            );
            END
            """
        ),
        {"db_username": db_username},
    )

    # getConfigurationForSystem
    conn.execute(
        text(
            """
            CREATE DEFINER=:db_username@`%` PROCEDURE `getConfigurationForSystem`(
            IN input_automation_system_name VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci
            )
            BEGIN
            SELECT conf.config_key, conf.config_value
            FROM `configurations` conf
            JOIN `automation_systems` asys
                ON conf.automation_system_id = asys.id
            WHERE asys.automation_system_name = input_automation_system_name
                ORDER BY conf.id ASC;

            END
            """
        ),
        {"db_username": db_username},
    )

    # getDetailsForDestinationPlate
    conn.execute(
        text(
            """
            CREATE DEFINER=:db_username@`%` PROCEDURE `getDetailsForDestinationPlate`(
            IN input_destination_barcode VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci
            )
            BEGIN
                SELECT slv.*
                FROM sample_level_view slv
                WHERE destination_barcode = input_destination_barcode
                ;

            END
            """
        ),
        {"db_username": db_username},
    )

    # doesSourcePlateExist
    conn.execute(
        text(
            """
            CREATE DEFINER=:db_username@`%` PROCEDURE `doesSourcePlateExist`(
            IN input_source_barcode VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci
            )
            BEGIN
                SELECT EXISTS(
                    SELECT id
                    FROM `source_plate_wells`
                    WHERE barcode = input_source_barcode
                );
            END
            """
        ),
        {"db_username": db_username},
    )

    # getPickableSamplesForSourcePlate
    conn.execute(
        text(
            """
            CREATE DEFINER=:db_username@`%` PROCEDURE `getPickableSamplesForSourcePlate`(
            IN input_source_barcode VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci
            )
            BEGIN
                SELECT
                    dpw.id AS destination_id,
                    spw.id,
                    spw.barcode,
                    spw.coordinate,
                    spw.sample_id,
                    spw.rna_id,
                    spw.lab_id
                FROM
                    `source_plate_wells` spw
                LEFT OUTER JOIN `destination_plate_wells` dpw
                    ON spw.id = dpw.source_plate_well_id
                WHERE
                    spw.barcode = input_source_barcode
                    AND dpw.id IS NULL
                ORDER BY spw.id;

            END
            """
        ),
        {"db_username": db_username},
    )

    # updateDestinationPlateWellWithControl
    conn.execute(
        text(
            """
            CREATE DEFINER=:db_username@`%` PROCEDURE `updateDestinationPlateWellWithControl`(
            IN input_automation_system_run_id INT,
            IN input_destination_barcode VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
            IN input_destination_coordinate VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
            IN input_control_plate_barcode VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
            IN input_control_coordinate VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci
            )
            BEGIN

            UPDATE `destination_plate_wells`
            SET
                control_plate_well_id = (
                SELECT id FROM `control_plate_wells` cpw
                WHERE cpw.automation_system_run_id = input_automation_system_run_id
                AND cpw.barcode = input_control_plate_barcode
                AND cpw.coordinate = input_control_coordinate
                ),
                updated_at = now()
            WHERE barcode = input_destination_barcode
            AND coordinate = input_destination_coordinate
            ;

            END
            """
        ),
        {"db_username": db_username},
    )

    # updateDestinationPlateWellWithSource
    conn.execute(
        text(
            """
            CREATE DEFINER=:db_username@`%` PROCEDURE `updateDestinationPlateWellWithSource`(
            IN input_automation_system_run_id INT,
            IN input_destination_barcode VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
            IN input_destination_coordinate VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
            IN input_source_plate_barcode VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
            IN input_source_coordinate VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci
            )
            BEGIN

            UPDATE `destination_plate_wells` dpw
            SET
                dpw.automation_system_run_id = input_automation_system_run_id,
                dpw.source_plate_well_id = (
                SELECT spw.id FROM `source_plate_wells` spw
                WHERE spw.barcode = input_source_plate_barcode
                AND spw.coordinate = input_source_coordinate
                ),
                dpw.updated_at = now()
            WHERE dpw.barcode = input_destination_barcode
            AND dpw.coordinate = input_destination_coordinate
            ;

            END
            """
        ),
        {"db_username": db_username},
    )

    # updateRunState
    conn.execute(
        text(
            """
            CREATE DEFINER=:db_username@`%` PROCEDURE `updateRunState`(
            IN input_automation_system_run_id INT,
            IN input_state ENUM('started','completed','aborted')
            )
            BEGIN

            UPDATE `automation_system_runs`
            SET
                end_time = CASE input_state
                            WHEN 'completed' THEN now()
                            WHEN 'aborted' THEN now()
                            ELSE end_time
                        END,
                state = input_state,
                updated_at = now()
            WHERE id = input_automation_system_run_id
            ;

            END
            """
        ),
        {"db_username": db_username},
    )


def downgrade():
    drop_stored_procedure("createControlPlateWellsRecord")
    drop_stored_procedure("createEmptyDestinationPlateWellsRecord")
    drop_stored_procedure("createRunEventRecord")
    drop_stored_procedure("createRunRecord")
    drop_stored_procedure("createSourcePlateWellRecord")
    drop_stored_procedure("getConfigurationForSystem")
    drop_stored_procedure("getDetailsForDestinationPlate")
    drop_stored_procedure("getPickableSamplesForSourcePlate")
    drop_stored_procedure("updateDestinationPlateWellWithControl")
    drop_stored_procedure("updateDestinationPlateWellWithSource")
    drop_stored_procedure("updateRunState")

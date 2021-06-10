"""Create stored procedures

Revision ID: ff18ff5a2ff6
Revises: b29f7af032f0
Create Date: 2021-06-10 10:31:24.371489

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "ff18ff5a2ff6"
down_revision = "b29f7af032f0"
branch_labels = None
depends_on = None


def drop_stored_procedure(procedure_name: str) -> None:
    if procedure_name is None or not procedure_name:
        raise Exception("Stored procedure name required to drop")

    op.execute(f"DROP PROCEDURE IF EXISTS `{procedure_name}`;")


def upgrade():
    # createControlPlateWellsRecord
    op.execute(
        """
        CREATE DEFINER=`root`@`%` PROCEDURE `createControlPlateWellsRecord`(
        IN input_automation_system_name VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
        IN input_system_run_id INT,
        IN input_barcode VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
        IN input_coordinate VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
        IN input_control VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
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
            (
            SELECT id FROM `automation_system_runs`
            WHERE automation_system_id = (
                SELECT id FROM `automation_systems`
                WHERE automation_system_name = input_automation_system_name
                )
            AND system_run_id = input_system_run_id
            ),
            input_barcode,
            input_coordinate,
            input_control,
            now(),
            now()
        );

        END
        """
    )

    # createEmptyDestinationPlateWellsRecord
    op.execute(
        """
        CREATE DEFINER=`root`@`%` PROCEDURE `createEmptyDestinationPlateWellsRecord`(
        IN input_automation_system_name VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
        IN input_system_run_id INT,
        IN input_barcode VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
        IN input_coordinate VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci

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
            ( SELECT id FROM `automation_system_runs`
            WHERE automation_system_id = (
                SELECT id FROM `automation_systems`
                WHERE automation_system_name = input_automation_system_name
                )
            AND system_run_id = input_system_run_id
            ),
            input_barcode,
            input_coordinate,
            NULL,
            NULL,
            now(),
            now()
        );

        END
        """
    )

    # createRunEventRecord
    op.execute(
        """
        CREATE DEFINER=`root`@`%` PROCEDURE `createRunEventRecord`(
        IN input_automation_system_name VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
        IN input_system_run_id INT,
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
            (
            SELECT id FROM `automation_system_runs`
            WHERE automation_system_id = (
                SELECT id FROM `automation_systems`
                WHERE automation_system_name = input_automation_system_name
            )
            AND system_run_id = input_system_run_id
            ),
            input_type,
            input_event,
            now(),
            now()
        );
        END
        """
    )

    # createRunRecord
    op.execute(
        """
        CREATE DEFINER=`root`@`%` PROCEDURE `createRunRecord`(
        IN input_automation_system_name VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
        IN input_system_run_id INT,
        IN input_gbg_method_name VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
        IN input_user_id VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
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

        SET @automationSystemRunId = '';
        SET @input_configuration = (
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
            system_run_id,
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
            input_system_run_id,
            input_gbg_method_name,
            input_user_id,
            now(),
            'started',
            now(),
            now()
        );

        SELECT LAST_INSERT_ID() INTO @automationSystemRunId;

        INSERT INTO `run_configurations` (
            automation_system_run_id,
            configuration_used,
            created_at,
            updated_at
        )
        VALUES (
            @automationSystemRunId,
            @input_configuration,
            now(),
            now()
        );

        -- Finish the transaction
        COMMIT;
        END
        """
    )

    # createSourcePlateWellRecord
    op.execute(
        """
        CREATE DEFINER=`root`@`%` PROCEDURE `createSourcePlateWellRecord`(
        IN input_barcode VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
        IN input_coordinate VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
        IN input_sample_id VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
        IN input_rna_id VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
        IN input_lab_id VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
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
    )

    # getConfigurationForSystem
    op.execute(
        """
        CREATE DEFINER=`root`@`%` PROCEDURE `getConfigurationForSystem`(
        IN input_automation_system_name VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
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
    )

    # getDetailsForDestinationPlate
    op.execute(
        """
        CREATE DEFINER=`root`@`%` PROCEDURE `getDetailsForDestinationPlate`(
        IN input_destination_barcode VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
        )
        BEGIN
            SELECT slv.*
            FROM sample_level_view slv
            WHERE destination_barcode = input_destination_barcode
            ;

        END
        """
    )

    # getLastSystemRunId
    op.execute(
        """
        CREATE DEFINER=`root`@`%` PROCEDURE `getLastSystemRunId`(
        OUT output_system_run_id int
        )
        BEGIN
            SELECT MAX(system_run_id)
            INTO output_system_run_id
            FROM automation_system_runs
            ;
        END
        """
    )

    # getPickableSamplesForSourcePlate
    op.execute(
        """
        CREATE DEFINER=`root`@`%` PROCEDURE `getPickableSamplesForSourcePlate`(
        IN input_source_barcode VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
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
    )

    # updateDestinationPlateWellWithControl
    op.execute(
        """
        CREATE DEFINER=`root`@`%` PROCEDURE `updateDestinationPlateWellWithControl`(
        IN input_automation_system_name VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
        IN input_system_run_id INT,
        IN input_destination_barcode VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
        IN input_destination_coordinate VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
        IN input_control_plate_barcode VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
        IN input_control_coordinate VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
        )
        BEGIN

        UPDATE `destination_plate_wells`
        SET
            control_plate_well_id = (
            SELECT id FROM `control_plate_wells` cpw
            WHERE cpw.automation_system_run_id = (
                SELECT id FROM `automation_system_runs`
                WHERE automation_system_id = (
                SELECT id FROM `automation_systems`
                    WHERE automation_system_name = input_automation_system_name
                )
                AND system_run_id = input_system_run_id
            )
            AND cpw.barcode = input_control_plate_barcode
            AND cpw.coordinate = input_control_coordinate
            ),
            updated_at = now()
        WHERE barcode = input_destination_barcode
        AND coordinate = input_destination_coordinate
        ;

        END
        """
    )

    # updateDestinationPlateWellWithSource
    op.execute(
        """
        CREATE DEFINER=`root`@`%` PROCEDURE `updateDestinationPlateWellWithSource`(
        IN input_automation_system_name VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
        IN input_system_run_id INT,
        IN input_destination_barcode VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
        IN input_destination_coordinate VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
        IN input_source_plate_barcode VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
        IN input_source_coordinate VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
        )
        BEGIN

        UPDATE `destination_plate_wells` dpw
        SET
            dpw.automation_system_run_id = (
            SELECT asr.id FROM `automation_system_runs` asr
            WHERE asr.automation_system_id = (
                SELECT asys.id FROM `automation_systems` asys
                WHERE asys.automation_system_name = input_automation_system_name
                )
            AND asr.system_run_id = input_system_run_id
            ),
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
    )

    # updateRunState
    op.execute(
        """
        CREATE DEFINER=`root`@`%` PROCEDURE `updateRunState`(
        IN input_automation_system_name VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
        IN input_system_run_id INT,
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
        WHERE automation_system_id = (
            SELECT id FROM `automation_systems`
            WHERE automation_system_name = input_automation_system_name
            )
        AND system_run_id = input_system_run_id
        ;

        END
        """
    )


def downgrade():
    drop_stored_procedure("createControlPlateWellsRecord")
    drop_stored_procedure("createEmptyDestinationPlateWellsRecord")
    drop_stored_procedure("createRunEventRecord")
    drop_stored_procedure("createRunRecord")
    drop_stored_procedure("createSourcePlateWellRecord")
    drop_stored_procedure("getConfigurationForSystem")
    drop_stored_procedure("getDetailsForDestinationPlate")
    drop_stored_procedure("getLastSystemRunId")
    drop_stored_procedure("getPickableSamplesForSourcePlate")
    drop_stored_procedure("updateDestinationPlateWellWithControl")
    drop_stored_procedure("updateDestinationPlateWellWithSource")
    drop_stored_procedure("updateRunState")

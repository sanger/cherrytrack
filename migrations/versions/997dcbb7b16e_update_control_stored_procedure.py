"""empty message

Revision ID: 997dcbb7b16e
Revises: 99363d3f06e9
Create Date: 2021-08-11 13:50:17.383267

"""

import sqlalchemy as sa
from alembic import op
from flask import current_app
from sqlalchemy.sql import text


# revision identifiers, used by Alembic.
revision = "997dcbb7b16e"
down_revision = "99363d3f06e9"
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

    drop_stored_procedure("updateDestinationPlateWellWithControl")

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
                automation_system_run_id = input_automation_system_run_id,
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


def downgrade():
    db_username = current_app.config["DATABASE_USERNAME"]

    # https://stackoverflow.com/a/23206636
    conn = op.get_bind()

    drop_stored_procedure("updateDestinationPlateWellWithControl")

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

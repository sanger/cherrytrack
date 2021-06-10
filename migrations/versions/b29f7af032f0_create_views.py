"""Create views

Revision ID: b29f7af032f0
Revises: 1bbe3ae5ec6d
Create Date: 2021-06-10 09:13:40.325027

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "b29f7af032f0"
down_revision = "1bbe3ae5ec6d"
branch_labels = None
depends_on = None


def drop_view(view_name: str) -> None:
    if view_name is None or not view_name:
        raise Exception("View name required to drop")

    op.execute(f"DROP VIEW IF EXISTS `{view_name}`;")


def upgrade():
    # https://alembic.sqlalchemy.org/en/latest/ops.html?highlight=execute#alembic.operations.Operations.execute

    # run_level_view
    op.execute(
        """
        CREATE VIEW `run_level_view` AS
            SELECT
                asys.automation_system_manufacturer,
                asys.automation_system_name,
                asys.liquid_handler_serial_number,
                asysr.system_run_id,
                asysr.method,
                asysr.user_id,
                asysr.start_time,
                asysr.end_time,
                TIMESTAMPDIFF(MINUTE,
                    asysr.start_time,
                    asysr.end_time) AS duration_minutes,
                state,
                (CASE asysr.state
                    WHEN 'started' THEN FALSE
                    WHEN 'aborted' THEN FALSE
                    WHEN 'completed' THEN TRUE
                END) AS completed_successfully,
                rc.configuration_used
            FROM
                `automation_system_runs` asysr
                    JOIN
                `automation_systems` asys ON asysr.automation_system_id = asys.id
                    JOIN
                `run_configurations` rc ON rc.automation_system_run_id = asysr.id
        ;
        """
    )

    # sample_level_view
    op.execute(
        """
        CREATE VIEW `sample_level_view` AS
            SELECT
                asys.automation_system_manufacturer,
                asys.automation_system_name,
                asysr.system_run_id,
                asysr.method,
                dpw.barcode AS destination_barcode,
                dpw.coordinate AS destination_coordinate,
                (CASE
                    WHEN spw.barcode IS NOT NULL THEN 'sample'
                    WHEN cpw.barcode IS NOT NULL THEN 'control'
                    ELSE 'empty'
                END) AS well_content_type,
                spw.barcode AS source_barcode,
                spw.coordinate AS source_coordinate,
                spw.rna_id,
                spw.lab_id,
                spw.sample_id,
                cpw.barcode AS control_barcode,
                cpw.coordinate AS control_coordinate,
                cpw.control
            FROM
                `automation_system_runs` asysr
                    JOIN
                `automation_systems` asys ON asysr.automation_system_id = asys.id
                    INNER JOIN
                `destination_plate_wells` dpw ON dpw.automation_system_run_id = asysr.id
                    LEFT OUTER JOIN
                `source_plate_wells` spw ON spw.id = dpw.source_plate_well_id
                    LEFT OUTER JOIN
                `control_plate_wells` cpw ON cpw.id = dpw.control_plate_well_id
        ;

        """
    )


def downgrade():
    drop_view("run_level_view")
    drop_view("sample_level_view")

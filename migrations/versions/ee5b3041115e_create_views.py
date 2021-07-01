"""Create Views

Revision ID: ee5b3041115e
Revises: 0740bd1e69ef
Create Date: 2021-07-01 16:21:41.828147

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "ee5b3041115e"
down_revision = "0740bd1e69ef"
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
              asysr.id AS automation_system_run_id,
              asysr.method,
              asysr.user_id,
              asysr.start_time,
              asysr.end_time,
              TIMESTAMPDIFF(
                  MINUTE,
                  asysr.start_time,
                  asysr.end_time
              ) AS duration_minutes,
              state,
              (CASE asysr.state
                  WHEN 'started' THEN false
                  WHEN 'aborted' THEN false
                  WHEN 'completed' THEN true
              END) AS completed_successfully,
              rc.configuration_used
          FROM `automation_system_runs` asysr
          JOIN `automation_systems` asys
              ON asysr.automation_system_id = asys.id
          JOIN `run_configurations` rc
              ON rc.automation_system_run_id = asysr.id
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
              asysr.id AS automation_system_run_id,
              asysr.method,
              dpw.barcode AS destination_barcode,
              dpw.coordinate AS destination_coordinate,
              (CASE
                  WHEN spw.barcode is not null THEN 'sample'
                  WHEN cpw.barcode is not null THEN 'control'
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
                  JOIN `automation_systems` asys
                      ON asysr.automation_system_id = asys.id
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

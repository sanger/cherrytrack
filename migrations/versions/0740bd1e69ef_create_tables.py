"""Create tables

Revision ID: 0740bd1e69ef
Revises:
Create Date: 2021-07-01 16:15:35.307607

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "0740bd1e69ef"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "automation_systems",
        sa.Column("id", sa.Integer(), nullable=False, comment="unique database identifier for this row"),
        sa.Column(
            "automation_system_name",
            sa.String(length=255, collation="utf8mb4_unicode_ci"),
            nullable=False,
            comment="the name for the workcell as used by the lab staff",
        ),
        sa.Column(
            "automation_system_manufacturer",
            sa.String(length=255, collation="utf8mb4_unicode_ci"),
            nullable=False,
            comment="used to distinguish groups of workcells supplied by different manufacturers",
        ),
        sa.Column(
            "liquid_handler_serial_number",
            sa.String(length=255, collation="utf8mb4_unicode_ci"),
            nullable=False,
            comment="the serial number of the liquid handler on the workcell",
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
            comment="the datetime when this row was created in the database",
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
            comment="the datetime when this row was updated in the database",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("automation_system_name"),
        comment="This table contains one row for each automation system (or workcell).",
    )
    op.create_table(
        "source_plate_wells",
        sa.Column("id", sa.Integer(), nullable=False, comment="unique database identifier for this row"),
        sa.Column(
            "barcode",
            sa.String(length=255, collation="utf8mb4_unicode_ci"),
            nullable=False,
            comment="the barcode for this plate, as scanned from the label",
        ),
        sa.Column(
            "coordinate",
            mysql.ENUM(
                "A1",
                "A2",
                "A3",
                "A4",
                "A5",
                "A6",
                "A7",
                "A8",
                "A9",
                "A10",
                "A11",
                "A12",
                "B1",
                "B2",
                "B3",
                "B4",
                "B5",
                "B6",
                "B7",
                "B8",
                "B9",
                "B10",
                "B11",
                "B12",
                "C1",
                "C2",
                "C3",
                "C4",
                "C5",
                "C6",
                "C7",
                "C8",
                "C9",
                "C10",
                "C11",
                "C12",
                "D1",
                "D2",
                "D3",
                "D4",
                "D5",
                "D6",
                "D7",
                "D8",
                "D9",
                "D10",
                "D11",
                "D12",
                "E1",
                "E2",
                "E3",
                "E4",
                "E5",
                "E6",
                "E7",
                "E8",
                "E9",
                "E10",
                "E11",
                "E12",
                "F1",
                "F2",
                "F3",
                "F4",
                "F5",
                "F6",
                "F7",
                "F8",
                "F9",
                "F10",
                "F11",
                "F12",
                "G1",
                "G2",
                "G3",
                "G4",
                "G5",
                "G6",
                "G7",
                "G8",
                "G9",
                "G10",
                "G11",
                "G12",
                "H1",
                "H2",
                "H3",
                "H4",
                "H5",
                "H6",
                "H7",
                "H8",
                "H9",
                "H10",
                "H11",
                "H12",
            ),
            nullable=False,
            comment="the coordinate of this well within the plate",
        ),
        sa.Column(
            "sample_id",
            sa.String(length=36, collation="utf8mb4_unicode_ci"),
            nullable=True,
            comment="the unique uuid identifier for the sample in this source well, passed through from the LIMS lookup API endpoint",
        ),
        sa.Column(
            "rna_id",
            sa.String(length=255, collation="utf8mb4_unicode_ci"),
            nullable=True,
            comment="the rna id identifier for the sample, passed through from the LIMS lookup API endpoint",
        ),
        sa.Column(
            "lab_id",
            sa.String(length=255, collation="utf8mb4_unicode_ci"),
            nullable=True,
            comment="the lighthouse lab id, passed through from the LIMS lookup API endpoint",
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
            comment="the datetime when this row was created in the database",
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
            comment="the datetime when this row was updated in the database",
        ),
        sa.PrimaryKeyConstraint("id"),
        comment="This table contains one row per pickable sample well per source plate.",
    )
    op.create_index(op.f("ix_source_plate_wells_barcode"), "source_plate_wells", ["barcode"], unique=False)
    op.create_index("source_plate_well", "source_plate_wells", ["barcode", "coordinate"], unique=True)
    op.create_table(
        "automation_system_runs",
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
            comment="unique database identifier for this row, used by biosero as automation_system_run_id",
        ),
        sa.Column(
            "automation_system_id",
            sa.Integer(),
            nullable=False,
            comment="the foreign key id from the automation systems table",
        ),
        sa.Column(
            "method",
            sa.String(length=255, collation="utf8mb4_unicode_ci"),
            nullable=False,
            comment="the name of the method running on the workcell, including a version number",
        ),
        sa.Column(
            "user_id",
            sa.String(length=255, collation="utf8mb4_unicode_ci"),
            nullable=False,
            comment="the user id of the lab staff member performing the run",
        ),
        sa.Column(
            "start_time",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
            comment="the date time when the run started",
        ),
        sa.Column(
            "end_time",
            sa.DateTime(),
            nullable=True,
            comment="the date time when the run ended, whether completed or aborted",
        ),
        sa.Column(
            "state", mysql.ENUM("started", "completed", "aborted"), nullable=False, comment="the state of the run"
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
            comment="the datetime when this row was created in the database",
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
            comment="the datetime when this row was updated in the database",
        ),
        sa.ForeignKeyConstraint(
            ["automation_system_id"],
            ["automation_systems.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        comment="This table contains one row per run on an automation system.",
    )
    op.create_index(
        op.f("ix_automation_system_runs_automation_system_id"),
        "automation_system_runs",
        ["automation_system_id"],
        unique=False,
    )
    op.create_table(
        "configurations",
        sa.Column("id", sa.Integer(), nullable=False, comment="unique database identifier for this row"),
        sa.Column(
            "automation_system_id",
            sa.Integer(),
            nullable=False,
            comment="the foreign key id from the automation systems table",
        ),
        sa.Column(
            "config_key",
            sa.String(length=255, collation="utf8mb4_unicode_ci"),
            nullable=False,
            comment="the key or name for this configuration key value pair",
        ),
        sa.Column(
            "config_value",
            sa.String(length=255, collation="utf8mb4_unicode_ci"),
            nullable=False,
            comment="the value for this configuration key value pair",
        ),
        sa.Column(
            "description",
            sa.String(length=255, collation="utf8mb4_unicode_ci"),
            nullable=False,
            comment="the description of what this key value pairing is used for",
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
            comment="the datetime when this row was created in the database",
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
            comment="the datetime when this row was updated in the database",
        ),
        sa.ForeignKeyConstraint(
            ["automation_system_id"],
            ["automation_systems.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        comment="This table contains one row per configuration key value pair for each automation system.",
    )
    op.create_index(
        "automation_system_config_key", "configurations", ["automation_system_id", "config_key"], unique=True
    )
    op.create_table(
        "control_plate_wells",
        sa.Column("id", sa.Integer(), nullable=False, comment="unique database identifier for this row"),
        sa.Column(
            "automation_system_run_id",
            sa.Integer(),
            nullable=False,
            comment="the foreign key id from the automation system runs table, uniquely identifying the run",
        ),
        sa.Column(
            "barcode",
            sa.String(length=255, collation="utf8mb4_unicode_ci"),
            nullable=False,
            comment="the barcode for this plate, as scanned from the label",
        ),
        sa.Column(
            "coordinate",
            mysql.ENUM(
                "A1",
                "A2",
                "A3",
                "A4",
                "A5",
                "A6",
                "A7",
                "A8",
                "A9",
                "A10",
                "A11",
                "A12",
                "B1",
                "B2",
                "B3",
                "B4",
                "B5",
                "B6",
                "B7",
                "B8",
                "B9",
                "B10",
                "B11",
                "B12",
                "C1",
                "C2",
                "C3",
                "C4",
                "C5",
                "C6",
                "C7",
                "C8",
                "C9",
                "C10",
                "C11",
                "C12",
                "D1",
                "D2",
                "D3",
                "D4",
                "D5",
                "D6",
                "D7",
                "D8",
                "D9",
                "D10",
                "D11",
                "D12",
                "E1",
                "E2",
                "E3",
                "E4",
                "E5",
                "E6",
                "E7",
                "E8",
                "E9",
                "E10",
                "E11",
                "E12",
                "F1",
                "F2",
                "F3",
                "F4",
                "F5",
                "F6",
                "F7",
                "F8",
                "F9",
                "F10",
                "F11",
                "F12",
                "G1",
                "G2",
                "G3",
                "G4",
                "G5",
                "G6",
                "G7",
                "G8",
                "G9",
                "G10",
                "G11",
                "G12",
                "H1",
                "H2",
                "H3",
                "H4",
                "H5",
                "H6",
                "H7",
                "H8",
                "H9",
                "H10",
                "H11",
                "H12",
            ),
            nullable=False,
            comment="the coordinate of this well within the plate",
        ),
        sa.Column(
            "control", mysql.ENUM("positive", "negative"), nullable=True, comment="the type of control in this well"
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
            comment="the datetime when this row was created in the database",
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
            comment="the datetime when this row was updated in the database",
        ),
        sa.ForeignKeyConstraint(
            ["automation_system_run_id"],
            ["automation_system_runs.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        comment="This table contains one row per pickable control well per control plate.",
    )
    op.create_index(
        "control_plate_well", "control_plate_wells", ["automation_system_run_id", "barcode", "coordinate"], unique=True
    )
    op.create_table(
        "run_configurations",
        sa.Column("id", sa.Integer(), nullable=False, comment="unique database identifier for this row"),
        sa.Column(
            "automation_system_run_id",
            sa.Integer(),
            nullable=False,
            comment="the foreign key id from the automation system runs table, uniquely identifying the run",
        ),
        sa.Column(
            "configuration_used",
            sa.JSON(),
            nullable=False,
            comment="the json representation of the configuration extracted from the configurations table that was used for this run",
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
            comment="the datetime when this row was created in the database",
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
            comment="the datetime when this row was updated in the database",
        ),
        sa.ForeignKeyConstraint(
            ["automation_system_run_id"],
            ["automation_system_runs.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("automation_system_run_id"),
        comment="This table contains one row per run to record the configuration settings used for that run.",
    )
    op.create_table(
        "run_events",
        sa.Column("id", sa.Integer(), nullable=False, comment="unique database identifier for this row"),
        sa.Column(
            "automation_system_run_id",
            sa.Integer(),
            nullable=False,
            comment="the foreign key id from the automation system runs table, uniquely identifying the run",
        ),
        sa.Column(
            "type", mysql.ENUM("info", "warning", "error"), nullable=True, comment="the type of the event being logged"
        ),
        sa.Column("event", sa.JSON(), nullable=False, comment="the json representation of the event information"),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
            comment="the datetime when this row was created in the database",
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
            comment="the datetime when this row was updated in the database",
        ),
        sa.ForeignKeyConstraint(
            ["automation_system_run_id"],
            ["automation_system_runs.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        comment="This table contains one row for each recorded event in a run.",
    )
    op.create_index(
        op.f("ix_run_events_automation_system_run_id"), "run_events", ["automation_system_run_id"], unique=False
    )
    op.create_table(
        "destination_plate_wells",
        sa.Column("id", sa.Integer(), nullable=False, comment="unique database identifier for this row"),
        sa.Column(
            "automation_system_run_id",
            sa.Integer(),
            nullable=False,
            comment="the foreign key id from the automation system runs table, uniquely identifying the run",
        ),
        sa.Column(
            "barcode",
            sa.String(length=255, collation="utf8mb4_unicode_ci"),
            nullable=False,
            comment="the barcode for this plate, as scanned from the label",
        ),
        sa.Column(
            "coordinate",
            mysql.ENUM(
                "A1",
                "A2",
                "A3",
                "A4",
                "A5",
                "A6",
                "A7",
                "A8",
                "A9",
                "A10",
                "A11",
                "A12",
                "B1",
                "B2",
                "B3",
                "B4",
                "B5",
                "B6",
                "B7",
                "B8",
                "B9",
                "B10",
                "B11",
                "B12",
                "C1",
                "C2",
                "C3",
                "C4",
                "C5",
                "C6",
                "C7",
                "C8",
                "C9",
                "C10",
                "C11",
                "C12",
                "D1",
                "D2",
                "D3",
                "D4",
                "D5",
                "D6",
                "D7",
                "D8",
                "D9",
                "D10",
                "D11",
                "D12",
                "E1",
                "E2",
                "E3",
                "E4",
                "E5",
                "E6",
                "E7",
                "E8",
                "E9",
                "E10",
                "E11",
                "E12",
                "F1",
                "F2",
                "F3",
                "F4",
                "F5",
                "F6",
                "F7",
                "F8",
                "F9",
                "F10",
                "F11",
                "F12",
                "G1",
                "G2",
                "G3",
                "G4",
                "G5",
                "G6",
                "G7",
                "G8",
                "G9",
                "G10",
                "G11",
                "G12",
                "H1",
                "H2",
                "H3",
                "H4",
                "H5",
                "H6",
                "H7",
                "H8",
                "H9",
                "H10",
                "H11",
                "H12",
            ),
            nullable=False,
            comment="the coordinate of this well within the plate",
        ),
        sa.Column(
            "source_plate_well_id",
            sa.Integer(),
            nullable=True,
            comment="the foreign key from the source plate wells table, uniquely identifying the source well picked into this destination well",
        ),
        sa.Column(
            "control_plate_well_id",
            sa.Integer(),
            nullable=True,
            comment="the foreign key from the control plate wells table, uniquely identifying the control well picked into this destination well",
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
            comment="the datetime when this row was created in the database",
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
            comment="the datetime when this row was updated in the database",
        ),
        sa.CheckConstraint("((`control_plate_well_id` = 1) xor (`source_plate_well_id` = 1))"),
        sa.ForeignKeyConstraint(
            ["automation_system_run_id"],
            ["automation_system_runs.id"],
        ),
        sa.ForeignKeyConstraint(
            ["control_plate_well_id"],
            ["control_plate_wells.id"],
        ),
        sa.ForeignKeyConstraint(
            ["source_plate_well_id"],
            ["source_plate_wells.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        comment="This table contains a row for each well in each destination plate, either empty or linked to a sample or control well once picked.",
    )
    op.create_index(op.f("ix_destination_plate_wells_barcode"), "destination_plate_wells", ["barcode"], unique=False)
    op.create_index(
        op.f("ix_destination_plate_wells_control_plate_well_id"),
        "destination_plate_wells",
        ["control_plate_well_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_destination_plate_wells_source_plate_well_id"),
        "destination_plate_wells",
        ["source_plate_well_id"],
        unique=False,
    )
    op.create_index(
        "run_destination_plate_well",
        "destination_plate_wells",
        ["automation_system_run_id", "barcode", "coordinate"],
        unique=True,
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("destination_plate_wells")
    op.drop_table("run_events")
    op.drop_table("run_configurations")
    op.drop_table("control_plate_wells")
    op.drop_table("configurations")
    op.drop_table("automation_system_runs")
    op.drop_table("source_plate_wells")
    op.drop_table("automation_systems")
    # ### end Alembic commands ###
# coding: utf-8
from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    JSON,
    String,
    text,
)

from sqlalchemy.dialects.mysql import ENUM
from sqlalchemy.orm import relationship

# from sqlalchemy.ext.declarative import declarative_base

from cherrytrack import db
from cherrytrack.constants import COORDINATES

# Base = declarative_base()
# metadata = Base.metadata

# Used sqlacodegen to generate models.py file from schema https://pypi.org/project/sqlacodegen/


# class AutomationSystem(Base):
class AutomationSystem(db.Model):  # type: ignore
    __tablename__ = "automation_systems"
    __table_args__ = {"comment": "This table contains one row for each automation system (or workcell)."}

    id = Column(Integer, primary_key=True, comment="unique database identifier for this row")
    automation_system_name = Column(
        String(255, "utf8mb4_unicode_ci"),
        nullable=False,
        unique=True,
        comment="the name for the workcell as used by the lab staff",
    )
    automation_system_manufacturer = Column(
        String(255, "utf8mb4_unicode_ci"),
        nullable=False,
        comment="used to distinguish groups of workcells supplied by different manufacturers",
    )
    liquid_handler_serial_number = Column(
        String(255, "utf8mb4_unicode_ci"),
        nullable=False,
        comment="the serial number of the liquid handler on the workcell",
    )
    created_at = Column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        comment="the datetime when this row was created in the database",
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        comment="the datetime when this row was updated in the database",
    )


# class SourcePlateWell(Base):
class SourcePlateWell(db.Model):  # type: ignore
    __tablename__ = "source_plate_wells"
    __table_args__ = (
        Index("source_plate_well", "barcode", "coordinate", unique=True),
        {"comment": "This table contains one row per pickable sample well per source plate."},
    )

    id = Column(Integer, primary_key=True, comment="unique database identifier for this row")
    barcode = Column(
        String(255, "utf8mb4_unicode_ci"),
        nullable=False,
        index=True,
        comment="the barcode for this plate, as scanned from the label",
    )
    coordinate = Column(
        ENUM(*COORDINATES),
        nullable=False,
        comment="the coordinate of this well within the plate",
    )
    sample_id = Column(
        String(36, "utf8mb4_unicode_ci"),
        comment=(
            "the unique uuid identifier for the sample in this source well, passed through from the LIMS lookup API "
            "endpoint"
        ),
    )
    rna_id = Column(
        String(255, "utf8mb4_unicode_ci"),
        comment="the rna id identifier for the sample, passed through from the LIMS lookup API endpoint",
    )
    lab_id = Column(
        String(255, "utf8mb4_unicode_ci"),
        comment="the lighthouse lab id, passed through from the LIMS lookup API endpoint",
    )
    created_at = Column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        comment="the datetime when this row was created in the database",
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        comment="the datetime when this row was updated in the database",
    )


# class AutomationSystemRun(Base):
class AutomationSystemRun(db.Model):  # type: ignore
    __tablename__ = "automation_system_runs"
    __table_args__ = {"comment": "This table contains one row per run on an automation system."}

    id = Column(
        Integer,
        primary_key=True,
        comment="unique database identifier for this row, used by biosero as automation_system_run_id",
    )
    automation_system_id = Column(
        ForeignKey("automation_systems.id"),
        nullable=False,
        index=True,
        comment="the foreign key id from the automation systems table",
    )
    method = Column(
        String(255, "utf8mb4_unicode_ci"),
        nullable=False,
        comment="the name of the method running on the workcell, including a version number",
    )
    user_id = Column(
        String(255, "utf8mb4_unicode_ci"),
        nullable=False,
        comment="the user id of the lab staff member performing the run",
    )
    start_time = Column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment="the date time when the run started"
    )
    end_time = Column(DateTime, comment="the date time when the run ended, whether completed or aborted")
    state = Column(ENUM("started", "completed", "aborted"), nullable=False, comment="the state of the run")
    created_at = Column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        comment="the datetime when this row was created in the database",
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        comment="the datetime when this row was updated in the database",
    )

    automation_system = relationship("AutomationSystem")


# class Configuration(Base):
class Configuration(db.Model):  # type: ignore
    __tablename__ = "configurations"
    __table_args__ = (
        Index("automation_system_config_key", "automation_system_id", "config_key", unique=True),
        {"comment": "This table contains one row per configuration key value pair for each automation system."},
    )

    id = Column(Integer, primary_key=True, comment="unique database identifier for this row")
    automation_system_id = Column(
        ForeignKey("automation_systems.id"),
        nullable=False,
        comment="the foreign key id from the automation systems table",
    )
    config_key = Column(
        String(255, "utf8mb4_unicode_ci"),
        nullable=False,
        comment="the key or name for this configuration key value pair",
    )
    config_value = Column(
        String(255, "utf8mb4_unicode_ci"), nullable=False, comment="the value for this configuration key value pair"
    )
    description = Column(
        String(255, "utf8mb4_unicode_ci"),
        nullable=False,
        comment="the description of what this key value pairing is used for",
    )
    created_at = Column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        comment="the datetime when this row was created in the database",
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        comment="the datetime when this row was updated in the database",
    )

    automation_system = relationship("AutomationSystem")


# class ControlPlateWell(Base):
class ControlPlateWell(db.Model):  # type: ignore
    __tablename__ = "control_plate_wells"
    __table_args__ = (
        Index("control_plate_well", "automation_system_run_id", "barcode", "coordinate", unique=True),
        {"comment": "This table contains one row per pickable control well per control plate."},
    )

    id = Column(Integer, primary_key=True, comment="unique database identifier for this row")
    automation_system_run_id = Column(
        ForeignKey("automation_system_runs.id"),
        nullable=False,
        comment="the foreign key id from the automation system runs table, uniquely identifying the run",
    )
    barcode = Column(
        String(255, "utf8mb4_unicode_ci"),
        nullable=False,
        comment="the barcode for this plate, as scanned from the label",
    )
    coordinate = Column(
        ENUM(*COORDINATES),
        nullable=False,
        comment="the coordinate of this well within the plate",
    )
    control = Column(ENUM("positive", "negative"), comment="the type of control in this well")
    created_at = Column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        comment="the datetime when this row was created in the database",
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        comment="the datetime when this row was updated in the database",
    )

    automation_system_run = relationship("AutomationSystemRun")


# class RunConfiguration(Base):
class RunConfiguration(db.Model):  # type: ignore
    __tablename__ = "run_configurations"
    __table_args__ = {
        "comment": "This table contains one row per run to record the configuration settings used for that run."
    }

    id = Column(Integer, primary_key=True, comment="unique database identifier for this row")
    automation_system_run_id = Column(
        ForeignKey("automation_system_runs.id"),
        nullable=False,
        unique=True,
        comment="the foreign key id from the automation system runs table, uniquely identifying the run",
    )
    configuration_used = Column(
        JSON,
        nullable=False,
        comment=(
            "the json representation of the configuration extracted from the configurations table that was used for "
            "this run"
        ),
    )
    created_at = Column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        comment="the datetime when this row was created in the database",
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        comment="the datetime when this row was updated in the database",
    )

    automation_system_run = relationship("AutomationSystemRun")


# class RunEvent(Base):
class RunEvent(db.Model):  # type: ignore
    __tablename__ = "run_events"
    __table_args__ = {"comment": "This table contains one row for each recorded event in a run."}

    id = Column(Integer, primary_key=True, comment="unique database identifier for this row")
    automation_system_run_id = Column(
        ForeignKey("automation_system_runs.id"),
        nullable=False,
        index=True,
        comment="the foreign key id from the automation system runs table, uniquely identifying the run",
    )
    type = Column(ENUM("info", "warning", "error"), comment="the type of the event being logged")
    event = Column(JSON, nullable=False, comment="the json representation of the event information")
    created_at = Column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        comment="the datetime when this row was created in the database",
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        comment="the datetime when this row was updated in the database",
    )

    automation_system_run = relationship("AutomationSystemRun")


# class DestinationPlateWell(Base):
class DestinationPlateWell(db.Model):  # type: ignore
    __tablename__ = "destination_plate_wells"
    __table_args__ = (
        CheckConstraint("((`control_plate_well_id` = 1) xor (`source_plate_well_id` = 1))"),
        Index("run_destination_plate_well", "automation_system_run_id", "barcode", "coordinate", unique=True),
        {
            "comment": (
                "This table contains a row for each well in each destination plate, either empty or linked to a sample "
                "or control well once picked."
            )
        },
    )

    id = Column(Integer, primary_key=True, comment="unique database identifier for this row")
    automation_system_run_id = Column(
        ForeignKey("automation_system_runs.id"),
        nullable=False,
        comment="the foreign key id from the automation system runs table, uniquely identifying the run",
    )
    barcode = Column(
        String(255, "utf8mb4_unicode_ci"),
        nullable=False,
        index=True,
        comment="the barcode for this plate, as scanned from the label",
    )
    coordinate = Column(
        ENUM(*COORDINATES),
        nullable=False,
        comment="the coordinate of this well within the plate",
    )
    source_plate_well_id = Column(
        ForeignKey("source_plate_wells.id"),
        index=True,
        comment=(
            "the foreign key from the source plate wells table, uniquely identifying the source well picked into this "
            "destination well"
        ),
    )
    control_plate_well_id = Column(
        ForeignKey("control_plate_wells.id"),
        index=True,
        comment=(
            "the foreign key from the control plate wells table, uniquely identifying the control well picked into "
            "this destination well"
        ),
    )
    created_at = Column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        comment="the datetime when this row was created in the database",
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        comment="the datetime when this row was updated in the database",
    )

    automation_system_run = relationship("AutomationSystemRun")
    control_plate_well = relationship("ControlPlateWell")
    source_plate_well = relationship("SourcePlateWell")

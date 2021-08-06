""" Update run_destination_plate_well Index

Revision ID: 99363d3f06e9
Revises: 06836ff03683
Create Date: 2021-08-06 15:44:38.573767

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "99363d3f06e9"
down_revision = "06836ff03683"
branch_labels = None
depends_on = None


def upgrade():
    # create index just on run, as there is a forign key constrait, a foreign key always requires an index
    op.create_index(
        "automation_system_run_id",
        "destination_plate_wells",
        ["automation_system_run_id"],
        unique=True,
    )

    # drop the index
    op.drop_index("run_destination_plate_well", "destination_plate_wells")

    # create the new index
    op.create_index(
        "destination_plate_well",
        "destination_plate_wells",
        ["barcode", "coordinate"],
        unique=True,
    )


def downgrade():
    # remove the new index
    op.drop_index("destination_plate_well", "destination_plate_wells")

    # recreate the old index
    op.create_index(
        "run_destination_plate_well",
        "destination_plate_wells",
        ["automation_system_run_id", "barcode", "coordinate"],
        unique=True,
    )

    # drop the run only index
    op.drop_index("automation_system_run_id", "destination_plate_wells")

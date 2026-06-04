"""add room table

Revision ID: 196c32702d3b
Revises: a73ae3cdafb1
Create Date: 2026-06-04 12:07:51.973523

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '196c32702d3b'
down_revision: Union[str, Sequence[str], None] = 'a73ae3cdafb1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    record_status = postgresql.ENUM(
        "ACTIVE",
        "INACTIVE",
        name="record_status",
        create_type=False,
    )

    op.create_table(
        "rooms",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("property_id", sa.Integer(), nullable=False),
        sa.Column("room_number", sa.String(length=50), nullable=False),
        sa.Column("room_type", sa.String(length=100), nullable=False),
        sa.Column("price_per_night", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column("capacity", sa.Integer(), nullable=False),
        sa.Column("availability", sa.Boolean(), nullable=False),
        sa.Column("status", record_status, nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["property_id"], ["properties.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "property_id",
            "room_number",
            name="uq_rooms_property_room_number",
        ),
    )
    op.create_index(op.f("ix_rooms_id"), "rooms", ["id"], unique=False)
    op.create_index(op.f("ix_rooms_property_id"), "rooms", ["property_id"], unique=False)
    op.create_index(op.f("ix_rooms_room_type"), "rooms", ["room_type"], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_rooms_room_type"), table_name="rooms")
    op.drop_index(op.f("ix_rooms_property_id"), table_name="rooms")
    op.drop_index(op.f("ix_rooms_id"), table_name="rooms")
    op.drop_table("rooms")

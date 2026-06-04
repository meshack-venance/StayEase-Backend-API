"""add upload image fields

Revision ID: 4c4307781969
Revises: 3df310b00ba4
Create Date: 2026-06-04 13:27:29.302801

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4c4307781969'
down_revision: Union[str, Sequence[str], None] = '3df310b00ba4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "users",
        sa.Column("profile_image_url", sa.String(length=500), nullable=True),
    )
    op.add_column(
        "properties",
        sa.Column("image_url", sa.String(length=500), nullable=True),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("properties", "image_url")
    op.drop_column("users", "profile_image_url")

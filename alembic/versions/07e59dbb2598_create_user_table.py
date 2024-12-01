"""create user table

Revision ID: 07e59dbb2598
Revises: be187399344f
Create Date: 2024-11-27 16:20:39.082930

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '07e59dbb2598'
down_revision: Union[str, None] = 'be187399344f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "user_table",
        sa.Column("user_id", sa.Integer, primary_key=True, nullable=False, autoincrement=True),
        sa.Column("username", sa.String, nullable=False, unique=True),
        sa.Column("email", sa.String, nullable=False, unique=True),
        sa.Column("password", sa.String, nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")),
    )


def downgrade() -> None:
    op.drop_table("user_table")

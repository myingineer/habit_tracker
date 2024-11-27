"""add columns for token and verification

Revision ID: 4b3db94dd615
Revises: 07e59dbb2598
Create Date: 2024-11-27 16:27:03.358298

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4b3db94dd615'
down_revision: Union[str, None] = '07e59dbb2598'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("user_table", sa.Column("token", sa.String, nullable=True))
    op.add_column("user_table", sa.Column("token_expiry", sa.TIMESTAMP, nullable=True))
    op.add_column("user_table", sa.Column("is_token_verified", sa.Boolean, nullable=False, server_default="false"))


def downgrade() -> None:
    op.drop_column("user_table", "is_token_verified")
    op.drop_column("user_table", "token_expiry")
    op.drop_column("user_table", "token")

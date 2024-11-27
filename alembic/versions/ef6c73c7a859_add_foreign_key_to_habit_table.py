"""add foreign key to habit table

Revision ID: ef6c73c7a859
Revises: 4b3db94dd615
Create Date: 2024-11-27 16:29:37.221681

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ef6c73c7a859'
down_revision: Union[str, None] = '4b3db94dd615'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "habit_table", 
        sa.Column("user_id", sa.Integer, sa.ForeignKey('user_table.user_id', ondelete='CASCADE'), nullable=False)
    )


def downgrade() -> None:
    op.drop_column("habit_table", "user_id")

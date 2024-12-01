"""create habit table

Revision ID: be187399344f
Revises: 
Create Date: 2024-11-27 14:32:49.476198

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from app.Schemas.habits_schemas import Periodicity


# revision identifiers, used by Alembic.
revision: str = 'be187399344f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:

    op.create_table(
        "habit_table",
        sa.Column("habit_id", sa.Integer, primary_key=True, nullable=False, autoincrement=True),
        sa.Column("habit", sa.String, nullable=False),
        sa.Column("periodicity", sa.Enum(Periodicity, name='periodicity'), nullable=False),
        sa.Column("description", sa.String, nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("date_to_complete", sa.Date, nullable=True),
    )


def downgrade() -> None:
    op.drop_table("habit_table")

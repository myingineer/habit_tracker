"""create remaining tables

Revision ID: cc2e63041e42
Revises: ef6c73c7a859
Create Date: 2024-11-27 16:42:00.487641

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from app.Schemas.habits_schemas import Periodicity


# revision identifiers, used by Alembic.
revision: str = 'cc2e63041e42'
down_revision: Union[str, None] = 'ef6c73c7a859'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('daily_habit_analytics',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('habit_id', sa.Integer(), nullable=False),
    sa.Column('streak_completed_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('streak_count', sa.Integer(), server_default=sa.text('0'), nullable=False),
    sa.ForeignKeyConstraint(['habit_id'], ['habit_table.habit_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('monthly_habit_analytics',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('habit_id', sa.Integer(), nullable=False),
    sa.Column('streak_completed_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('streak_count', sa.Integer(), server_default=sa.text('0'), nullable=False),
    sa.ForeignKeyConstraint(['habit_id'], ['habit_table.habit_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('streak_analytics',
    sa.Column('habit_id', sa.Integer(), nullable=False),
    sa.Column('current_streak_count', sa.Integer(), server_default=sa.text('0'), nullable=False),
    sa.Column('longest_streak_count', sa.Integer(), server_default=sa.text('0'), nullable=False),
    sa.Column('periodicity', sa.Enum(Periodicity, name='periodicity'), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('daily_last_updated', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('weekly_last_updated', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('monthly_last_updated', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['habit_id'], ['habit_table.habit_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user_table.user_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('habit_id'),
    sa.UniqueConstraint('habit_id')
    )
    op.create_table('weekly_habit_analytics',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('habit_id', sa.Integer(), nullable=False),
    sa.Column('streak_completed_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('streak_count', sa.Integer(), server_default=sa.text('0'), nullable=False),
    sa.ForeignKeyConstraint(['habit_id'], ['habit_table.habit_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('weekly_habit_analytics')
    op.drop_table('streak_analytics')
    op.drop_table('monthly_habit_analytics')
    op.drop_table('daily_habit_analytics')
    # ### end Alembic commands ###

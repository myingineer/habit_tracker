from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, text, Enum as SQLAlchemyEnum
from ..Schemas.habits_schemas import Periodicity
from ..Models import Base

class Analytic(Base):
    __tablename__ = "streak_analytics"

    habit_id = Column(Integer, ForeignKey('habit_table.habit_id', ondelete='CASCADE'), primary_key=True, nullable=False, unique=True)
    current_streak_count = Column(Integer, nullable=False, server_default=text('0'))
    longest_streak_count = Column(Integer, nullable=False, server_default=text('0'))
    periodicity = Column(SQLAlchemyEnum(Periodicity, name='periodicity'), nullable=False)
    user_id = Column(Integer, ForeignKey('user_table.user_id', ondelete='CASCADE'), nullable=False)
    daily_last_updated = Column(TIMESTAMP(timezone=True), nullable=True)
    weekly_last_updated = Column(TIMESTAMP(timezone=True), nullable=True)
    monthly_last_updated = Column(TIMESTAMP(timezone=True), nullable=True)


class AnalyticsDaily(Base):
    __tablename__ = "daily_habit_analytics"

    id = Column(Integer, primary_key=True, nullable=False)
    habit_id = Column(Integer, ForeignKey('habit_table.habit_id', ondelete='CASCADE'), nullable=False)
    streak_completed_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    streak_count = Column(Integer, nullable=False, server_default=text('0'))

class AnalyticsWeekly(Base):
    __tablename__ = "weekly_habit_analytics"

    id = Column(Integer, primary_key=True, nullable=False)
    habit_id = Column(Integer, ForeignKey('habit_table.habit_id', ondelete='CASCADE'), nullable=False)
    streak_completed_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    streak_count = Column(Integer, nullable=False, server_default=text('0'))

class AnalyticsMonthly(Base):
    __tablename__ = "monthly_habit_analytics"

    id = Column(Integer, primary_key=True, nullable=False)
    habit_id = Column(Integer, ForeignKey('habit_table.habit_id', ondelete='CASCADE'), nullable=False)
    streak_completed_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    streak_count = Column(Integer, nullable=False, server_default=text('0'))

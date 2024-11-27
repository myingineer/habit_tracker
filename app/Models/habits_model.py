from sqlalchemy import Column, Date, ForeignKey, Integer, String, Enum as SQLAlchemyEnum
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from ..Schemas.habits_schemas import Periodicity
from ..Models import Base

class Habit(Base):
    __tablename__ = "habit_table"
    
    habit_id = Column(Integer, primary_key=True, nullable=False)
    habit = Column(String, nullable=False)
    periodicity = Column(SQLAlchemyEnum(Periodicity, name='periodicity'), nullable=False)
    description = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    date_to_complete = Column(Date, nullable=True) # Date is in the format YYYY-MM-DD
    user_id = Column(Integer, ForeignKey('user_table.user_id', ondelete='CASCADE'), nullable=False)
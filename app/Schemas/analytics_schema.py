from pydantic import BaseModel
from .habits_schemas import Periodicity

# Analytic Base Model Schema
class AnalyticBase(BaseModel):
    habit_id: int
    current_streak_count: int
    longest_streak_count: int
    periodicity: Periodicity

# Streak Populate Schema
class Streak(BaseModel):
    habit_id: int


# Analytic Response Schema
class AnalyticResponse(AnalyticBase):
    user_id: int
    habit: str
    description: str

    class Config:
        from_attributes = True
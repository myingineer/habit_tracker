from datetime import datetime, date
from enum import Enum
from pydantic import BaseModel
from typing import Optional

# Periodicity Users can choose from
class Periodicity(str, Enum):
    Daily = "daily" 
    Weekly = "weekly" 
    Monthly = "monthly" 

# Habit Base Model Schema
class HabitBase(BaseModel):
    habit: str
    periodicity: Periodicity
    description: str

# Habit Create Schema
class HabitCreate(HabitBase):
    date_to_complete: Optional[date] = None

# Habit Update Schema make all fields optional
class HabitUpdate(BaseModel):
    description: Optional[str] = None
    date_to_complete: Optional[date] = None

# Habit Schema used also for response
class Habit(HabitBase):
    habit_id: int
    created_at: datetime
    date_to_complete: Optional[date] = None
    user_id: int

    class ConfigDict:
        from_attributes = True
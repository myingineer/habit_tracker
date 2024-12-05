from typing import List
from fastapi import APIRouter, Response, status, Depends, HTTPException
from ..Schemas import habits_schemas
from fastapi.params import Body
from ..Utils import database, oauth2, validators
from sqlalchemy.orm import Session
from ..Models import habits_model


router = APIRouter(
    tags=["Habits"],
    prefix="/habits"
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=habits_schemas.Habit)
async def createHabit(habit: habits_schemas.HabitCreate = Body(...), db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_habit = habits_model.Habit(user_id = current_user.user_id, **habit.model_dump())

    db.add(new_habit)
    db.commit()
    db.refresh(new_habit)

    return new_habit

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[habits_schemas.Habit])
async def getAllHabits(db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    habits = db.query(habits_model.Habit).filter(habits_model.Habit.user_id == current_user.user_id).all()
    return habits

@router.get("/{habit_id}", status_code=status.HTTP_200_OK, response_model=habits_schemas.Habit)
async def getHabit(habit_id: int, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    habit = db.query(habits_model.Habit).filter(habits_model.Habit.habit_id == habit_id).first()

    await validators.Validator_Functions.habit_exist(habit, habit_id)
    await validators.Validator_Functions.confirm_permission(habit.user_id, current_user.user_id)
    
    return habit


@router.patch("/{habit_id}", status_code=status.HTTP_200_OK, response_model=habits_schemas.Habit)
async def updateHabit(habit_id: int, habit_fields_to_update: habits_schemas.HabitUpdate, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    habit_query = db.query(habits_model.Habit).filter(habits_model.Habit.habit_id == habit_id)
    habit = habit_query.first()

    await validators.Validator_Functions.habit_exist(habit, habit_id)
    await validators.Validator_Functions.confirm_permission(habit.user_id, current_user.user_id)

    update_data = habit_fields_to_update.model_dump(exclude_unset=True)

    if not update_data:
        available_fields = list(habits_schemas.HabitUpdate.model_fields.keys())
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No valid fields to update. Valid fields are {available_fields}"
        )
    
    for key, value in update_data.items():
        setattr(habit, key, value)

    db.commit()
    db.refresh(habit)

    return habit

@router.delete("/{habit_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deleteHabit(habit_id: int, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    habit_query = db.query(habits_model.Habit).filter(habits_model.Habit.habit_id == habit_id)
    habit = habit_query.first()

    await validators.Validator_Functions.habit_exist(habit, habit_id)
    await validators.Validator_Functions.confirm_permission(habit.user_id, current_user.user_id)

    db.delete(habit)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
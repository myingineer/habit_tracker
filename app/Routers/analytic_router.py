from datetime import datetime, timezone
from fastapi import APIRouter, status, Depends, Query
from sqlalchemy.orm import Session
from ..Utils import database, oauth2, validators, analytic_helper
from ..Models import analytics_model, habits_model
from ..Schemas import analytics_schema, habits_schemas, users_schemas


router = APIRouter(
    tags=["Analytics"],
    prefix="/analytics"
)

# Update the streak count
@router.post("/streak/update", status_code=status.HTTP_200_OK, response_model=analytics_schema.AnalyticResponse)
async def update_streak(
    streak_data: analytics_schema.Streak,
    db: Session = Depends(database.get_db),
    current_user: users_schemas.User = Depends(oauth2.get_current_user)
):
    
    habit = db.query(habits_model.Habit).filter(habits_model.Habit.habit_id == streak_data.habit_id).first()
    await validators.Validator_Functions.habit_exist(habit, streak_data.habit_id)
    await validators.Validator_Functions.confirm_permission(habit.user_id, current_user.user_id)

    # Update the streak
    response = await analytic_helper.update_streak_count(streak_data, current_user, db, habits_model, analytics_model)

    # Save the streak data to be used for analytics later
    data = {
        "habit_id": habit.habit_id,
        "streak_completed_at": datetime.now(timezone.utc),
        "streak_count": response['current_streak_count']
    }

    # Save the data to the appropriate table
    if habit.periodicity == habits_schemas.Periodicity.Daily:
        db.add(analytics_model.AnalyticsDaily(**data))
        db.commit()
    elif habit.periodicity == habits_schemas.Periodicity.Weekly:
        db.add(analytics_model.AnalyticsWeekly(**data))
        db.commit()
    elif habit.periodicity == habits_schemas.Periodicity.Monthly:
        db.add(analytics_model.AnalyticsMonthly(**data))
        db.commit()
        
    return response

# Get all analytics data/streaks
@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_analytics_data(db: Session = Depends(database.get_db), current_user: users_schemas.User = Depends(oauth2.get_current_user), periodicity: habits_schemas.Periodicity = Query(None, description="Filter habits by periodicity")):

    analysis = db.query(analytics_model.Analytic).filter(analytics_model.Analytic.user_id == current_user.user_id).all()
    habits_query = db.query(habits_model.Habit).filter(habits_model.Habit.user_id == current_user.user_id)

    if periodicity:
        habits_query = habits_query.filter(habits_model.Habit.periodicity == periodicity)
    
    habits = habits_query.all()

    habit_map = {habit.habit_id: {"name": habit.habit, "description": habit.description} for habit in habits}

    response_data = []
    for analytic in analysis:
        # As we loop through the analytics data, we can get the habit information from the habit_map
        habit_info = habit_map.get(analytic.habit_id)
        if habit_info:
            # Then we append each analytic data to the response_data list
            response_data.append(analytics_schema.AnalyticResponse(
                habit_id=analytic.habit_id,
                current_streak_count=analytic.current_streak_count,
                longest_streak_count=analytic.longest_streak_count,
                periodicity=analytic.periodicity,
                user_id=current_user.user_id,
                habit=habit_info['name'],
                description=habit_info['description']
            ))
        
    if not response_data:
        await validators.Validator_Functions.general_error("No analytics data found", status.HTTP_404_NOT_FOUND)

    return response_data

# Get all analytics data/streaks for a specific habit
@router.get("/{habit_id}", status_code=status.HTTP_200_OK)
async def get_specific_analytics_data(habit_id: int, db: Session = Depends(database.get_db), current_user: users_schemas.User = Depends(oauth2.get_current_user)):

    habit = db.query(habits_model.Habit).filter(habits_model.Habit.habit_id == habit_id).first()
    await validators.Validator_Functions.habit_exist(habit, habit_id)
    await validators.Validator_Functions.confirm_permission(habit.user_id, current_user.user_id)

    analysis = db.query(analytics_model.Analytic).filter(analytics_model.Analytic.habit_id == habit_id).first()
    habit_info = {
        "name": habit.habit,
        "description": habit.description
    }

    response_data = analytics_schema.AnalyticResponse(
        habit_id=analysis.habit_id,
        current_streak_count=analysis.current_streak_count,
        longest_streak_count=analysis.longest_streak_count,
        periodicity=analysis.periodicity,
        user_id=current_user.user_id,
        habit=habit_info['name'],
        description=habit_info['description']
    )

    return response_data


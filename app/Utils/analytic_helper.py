from .validators import Validator_Functions
from datetime import datetime, timedelta, timezone, date
from ..Schemas import habits_schemas
from fastapi import HTTPException, status
from ..Schemas import analytics_schema, users_schemas
from ..Models import habits_model, analytics_model

async def update_streak_count(
    streak_data: analytics_schema.Streak,
    current_user: users_schemas.User, 
    db,
    habits_model: habits_model.Habit,
    analytics_model: analytics_model.Analytic,
):
    # Check if the habit exists
    habit = db.query(habits_model.Habit).filter(habits_model.Habit.habit_id == streak_data.habit_id).first()
    await Validator_Functions.habit_exist(habit, streak_data.habit_id)
    await Validator_Functions.confirm_permission(habit.user_id, current_user.user_id)

    # Compares the user expected date to complete the habit with the current date
    if habit.date_to_complete and habit.date_to_complete <= date.today():
        await Validator_Functions.general_error("Habit has already been completed")


    # Check if the streak exists
    analytic = db.query(analytics_model.Analytic).filter(
        analytics_model.Analytic.habit_id == streak_data.habit_id,
        analytics_model.Analytic.user_id == current_user.user_id
    ).first()
    
    current_time = datetime.now(timezone.utc)
    # Check if the user can update the streak
    can_update = False

    if analytic:
        if habit.periodicity == habits_schemas.Periodicity.Daily:
            next_update_time = (analytic.daily_last_updated + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
            if analytic.daily_last_updated is None or current_time >= next_update_time:
                can_update = True

        elif habit.periodicity == habits_schemas.Periodicity.Weekly:
            next_update_time = (analytic.weekly_last_updated + timedelta(weeks=1)).replace(hour=0, minute=0, second=0, microsecond=0)
            if analytic.weekly_last_updated is None or current_time >= next_update_time:
                if analytic.weekly_last_updated < (current_time - timedelta(days=current_time.weekday())):
                    can_update = True

        elif habit.periodicity == habits_schemas.Periodicity.Monthly:
            next_update_time = (analytic.monthly_last_updated + timedelta(days=30)).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            if analytic.monthly_last_updated is None or current_time >= next_update_time:
                if analytic.monthly_last_updated.month < current_time.month or analytic.monthly_last_updated.year < current_time.year:
                    can_update = True

        if can_update:
            # If the user can update the streak, we update the streak count
            analytic.current_streak_count += 1
            # If the current streak count is greater than the longest streak count, we update the longest streak count
            if analytic.current_streak_count > analytic.longest_streak_count:
                analytic.longest_streak_count = analytic.current_streak_count
            
            # Update the last updated time based on the periodicity of the habit
            if habit.periodicity == habits_schemas.Periodicity.Daily:
                analytic.daily_last_updated = current_time
            elif habit.periodicity == habits_schemas.Periodicity.WEEKLY:
                analytic.weekly_last_updated = current_time
            elif habit.periodicity == habits_schemas.Periodicity.MONTHLY:
                analytic.monthly_last_updated = current_time
        else:
            # Error if user tries to update the streak before the next allowed period
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Update not allowed. Please wait for the next allowed period.")
    else:
        # If the analytic data does not exist, we create a new analytic data for the user
        
        analytic = analytics_model.Analytic(
            habit_id=streak_data.habit_id,
            current_streak_count=1,
            longest_streak_count=1,
            periodicity=habit.periodicity,
            user_id=current_user.user_id,
            daily_last_updated=current_time if habit.periodicity == habits_schemas.Periodicity.Daily else None,
            weekly_last_updated=current_time if habit.periodicity == habits_schemas.Periodicity.Weekly else None,
            monthly_last_updated=current_time if habit.periodicity == habits_schemas.Periodicity.Monthly else None
        )
        db.add(analytic)

    db.commit()
    db.refresh(analytic)

    # Create the response data following the schema
    response_data = {
        "habit_id": analytic.habit_id,
        "current_streak_count": analytic.current_streak_count,
        "longest_streak_count": analytic.longest_streak_count,
        "periodicity": analytic.periodicity,
        "user_id": current_user.user_id,
        "habit": habit.habit,
        "description": habit.description
    }

    return response_data
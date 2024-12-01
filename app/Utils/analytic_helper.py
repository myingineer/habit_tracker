from .validators import Validator_Functions
from datetime import datetime, timedelta, timezone, date
from ..Schemas import habits_schemas
from fastapi import HTTPException, status
from ..Schemas import analytics_schema, users_schemas
from ..Models import habits_model, analytics_model


def refresh_streak_and_time(analytic, habit, current_time):
    """
    Updates streak counts and last updated time for the habit's periodicity.
    """
    # Increment current streak
    analytic.current_streak_count += 1

    # Update longest streak if needed
    if analytic.current_streak_count > analytic.longest_streak_count:
        analytic.longest_streak_count = analytic.current_streak_count

    # Mapping to update the appropriate last_updated field
    periodicity_map = {
        habits_schemas.Periodicity.Daily: "daily_last_updated",
        habits_schemas.Periodicity.Weekly: "weekly_last_updated",
        habits_schemas.Periodicity.Monthly: "monthly_last_updated"
    }

    # Dynamically set the last updated time
    last_updated_field = periodicity_map.get(habit.periodicity)
    if last_updated_field:
        setattr(analytic, last_updated_field, current_time)

    return True


def is_streak_missed(last_updated, periodicity, current_time):
    if periodicity == habits_schemas.Periodicity.Daily:
        # Missed streak if the last update was not yesterday or today
        yesterday = (current_time - timedelta(days=1)).date()
        return last_updated.date() < yesterday

    elif periodicity == habits_schemas.Periodicity.Weekly:
        # Missed streak if the last update was not within the last 7 days
        last_week_start = (current_time - timedelta(days=7)).date()
        return last_updated.date() < last_week_start

    elif periodicity == habits_schemas.Periodicity.Monthly:
        # Missed streak if the last update was not within the last calendar month
        last_month = (current_time.month - 1) or 12
        last_month_year = current_time.year if current_time.month != 1 else current_time.year - 1
        return last_updated.year < last_month_year or last_updated.month < last_month

    return False  # Default case, should not occur

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

    
    if analytic:
        last_update = None
        next_update_time = None

        # Calculate the next update time based on the habit's periodicity
        if habit.periodicity == habits_schemas.Periodicity.Daily:
            last_update = analytic.daily_last_updated or datetime.min
            next_update_time = (last_update + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)

        elif habit.periodicity == habits_schemas.Periodicity.Weekly:
            last_update = analytic.weekly_last_updated or datetime.min
            next_update_time = (last_update + timedelta(weeks=1)).replace(hour=0, minute=0, second=0, microsecond=0)

        elif habit.periodicity == habits_schemas.Periodicity.Monthly:
            last_update = analytic.monthly_last_updated or datetime.min
            next_month = (last_update.month % 12) + 1
            next_year = last_update.year + (1 if next_month == 1 else 0)
            next_update_time = last_update.replace(year=next_year, month=next_month, day=1, hour=0, minute=0, second=0, microsecond=0)

        # Check if the streak was missed
        if is_streak_missed(last_update, habit.periodicity, current_time):
            analytic.current_streak_count = 0
            
        # Check if the update is allowed
        if current_time >= next_update_time:
            refresh_streak_and_time(analytic, habit, current_time)
        else:
            await Validator_Functions.general_error(f"Habit with ID: {streak_data.habit_id} can only be updated after {next_update_time}")
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
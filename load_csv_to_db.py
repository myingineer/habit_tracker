import pandas as pd
from sqlalchemy.orm import Session
from app.Utils.database import engine, get_db
from sqlalchemy import text


# List of your tables and corresponding CSV files
tables_and_files = [
    ('user_table', 'csv/user_table.csv'),
    ('habit_table', 'csv/habit_table.csv'),
    ('daily_habit_analytics', 'csv/daily_habit_analytics.csv'),
    ('weekly_habit_analytics', 'csv/weekly_habit_analytics.csv'),
    ('streak_analytics', 'csv/streak_analytics.csv')
]

# Function to load CSV into the PostgreSQL database
def load_csv_to_postgresql(db: Session):
    for table, csv_file in tables_and_files:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(csv_file)

        # Save the data to PostgreSQL, append mode
        df.to_sql(table, con=engine, if_exists='append', index=False)
        print(f"Data from {csv_file} loaded into {table}.")
        
        # Reset the sequence for auto-incremented fields (optional)
        reset_sequence(db, table)


# Function to reset the sequence for auto-increment fields
def reset_sequence(db: Session, table: str):
    if table == 'habit_table':
        db.execute(text("""
            SELECT setval(pg_get_serial_sequence('habit_table', 'habit_id'), max(habit_id)) FROM habit_table;
        """))
        print("Sequence for habit_table reset.")
    
    if table == 'user_table':
        db.execute(text("""
            SELECT setval(pg_get_serial_sequence('user_table', 'user_id'), max(user_id)) FROM user_table;
        """))
        print("Sequence for user_table reset.")
    
    if table == 'daily_habit_analytics':
        db.execute(text("""
            SELECT setval(pg_get_serial_sequence('daily_habit_analytics', 'id'), max(id)) FROM daily_habit_analytics;
        """))
        print("Sequence for daily_habit_analytics reset.")
    
    if table == 'monthly_habit_analytics':
        db.execute(text("""
            SELECT setval(pg_get_serial_sequence('monthly_habit_analytics', 'id'), max(id)) FROM monthly_habit_analytics;
        """))
        print("Sequence for monthly_habit_analytics reset.")
    
    if table == 'weekly_habit_analytics':
        db.execute(text("""
            SELECT setval(pg_get_serial_sequence('weekly_habit_analytics', 'id'), max(id)) FROM weekly_habit_analytics;
        """))
        print("Sequence for weekly_habit_analytics reset.")



# Manually create a session for this script
if __name__ == "__main__":
    # Getting the DB session using the `get_db` function manually
    db = next(get_db())  # Assuming `get_db()` yields a session
    try:
        # Execute the function that loads data into the DB
        load_csv_to_postgresql(db)
    except Exception as e:
        print(f"Error while loading data: {e}")
    finally:
        db.close()  # Closing the session when done

    # Dispose of the engine connection when done
    engine.dispose()






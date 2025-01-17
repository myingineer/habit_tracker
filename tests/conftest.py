from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.Utils.config import settings
from app.Utils.database import get_db
from app import Models
from app.Utils import oauth2


# Testing Database URL
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DB_USERNAME}:{settings.DB_PASSWORD}@{settings.DB_URL}:{settings.DB_PORT}/{settings.DB_NAME}_test"

# Create the database engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a session local for testing
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a test session for the database
@pytest.fixture()
def db_session():
    # Before the test, drop the tables and recreate them
    Models.Base.metadata.drop_all(bind=engine)
    Models.Base.metadata.create_all(bind=engine)

    # Create a test session
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a test client. Calling the client with automatically call  the db_session fixture
@pytest.fixture()
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    # Override the get_db dependency so that the test session is used
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

# Create a test user for testing the login route making it independent of the signup route
@pytest.fixture()
def test_user(client):
    user_data = {
        "username": "test_user",
        "email":  "test_email@test.com",
        "password": "test_password"
    }
    response = client.post("/users/signup", json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user

# Create a test user token without using the full login route
@pytest.fixture()
def token(test_user):
    return oauth2.create_access_token({"user_id": test_user["user_id"]})

# Create a client with the authorization header set
@pytest.fixture()
def authorized_client(client, token):
    client.headers["Authorization"] = f"Bearer {token}"
    return client

# Create a test habit
@pytest.fixture()
def test_habits(test_user, db_session):
    habits_data = [
        {
            "habit": "Test Habit 1",
            "description": "Test Description 1",
            "periodicity": "daily",
            "user_id": test_user["user_id"]
        },
        {
            "habit": "Test Habit 2",
            "description": "Test Description 2",
            "periodicity": "weekly",
            "user_id": test_user["user_id"]
        }
    ]
    db_session.add_all([Models.Habit(**habit) for habit in habits_data])
    db_session.commit()
    habits = db_session.query(Models.Habit).all()
    return habits

# Create a test analytics data for testing the analytics route
@pytest.fixture()
def test_analytics(test_habits, db_session):
    # Testing data for the analytic table
    analytics_data = [
        {
            "habit_id": test_habits[0].habit_id,
            "current_streak_count": 10,
            "longest_streak_count": 10,
            "periodicity": "daily",
            "user_id": test_habits[0].user_id,
            "daily_last_updated": "2021-01-01 00:00:00",
            "weekly_last_updated": None,
            "monthly_last_updated": None
        },
        {
            "habit_id": test_habits[1].habit_id,
            "current_streak_count": 5,
            "longest_streak_count": 5,
            "periodicity": "weekly",
            "user_id": test_habits[1].user_id,
            "daily_last_updated": None,
            "weekly_last_updated": "2021-01-01 00:00:00",
            "monthly_last_updated": None
        }
    ]

    # Testing data for the daily analytics table
    daily_analytics_data = [
        {
            "habit_id": test_habits[0].habit_id,
            "streak_completed_at": "2021-01-01 00:00:00",
            "streak_count": 10
        }
    ]
    
    # Testing data for the weekly analytics table
    weekly_analytics_data = [
        {
            "habit_id": test_habits[1].habit_id,
            "streak_completed_at": "2021-01-01 00:00:00",
            "streak_count": 5
        }
    ]

    db_session.add_all([Models.Analytic(**data) for data in analytics_data])

    """
        Upon adding data to the streak_analytics table, the corresponding streak data must be added to
        either the daily or weekly analytics table to store the data at the point of completion for the appropriate periodicity.

        That is why we are looping through.
    """
    for data in analytics_data:
        if data["periodicity"] == "daily":
            db_session.add_all([Models.AnalyticsDaily(**entry) for entry in daily_analytics_data])
        elif data["periodicity"] == "weekly":
            db_session.add_all([Models.AnalyticsWeekly(**entry) for entry in weekly_analytics_data])


    db_session.commit()
    analytics = db_session.query(Models.Analytic).all()
    return analytics
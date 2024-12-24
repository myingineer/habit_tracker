from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.Utils.config import settings
from app.Utils.database import get_db
from app import Models


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

# Create a test client
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

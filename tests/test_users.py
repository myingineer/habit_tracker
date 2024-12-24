from app.Schemas import users_schemas
from jose import jwt
from app.Utils.config import settings
import pytest

# Test the create user route
def test_create_user(client):
    response = client.post("/users/signup", json={
        "username": "test_user",
        "email":  "test_email@test.com",
        "password": "test_password"
    })
    assert response.status_code == 201

# Test the login route
def test_login(client, test_user):
    response = client.post("/users/login", data={
        "username": test_user["username"],
        "password": test_user["password"]
    })
    # Make sure the response matches the Token schema
    login_response = users_schemas.Token(**response.json())
    # Decode the token to get the user
    payload = jwt.decode(login_response.access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

    # Get the user_id from the token
    user_id: int = payload.get("user_id")
    assert user_id == test_user["user_id"]
    assert login_response.token_type == "Bearer"
    assert response.status_code == 200


# Test wrong login credentials
@pytest.mark.parametrize("username, password, status_code", [
    ("test_user", "wrong_password", 403),
    ("wrong_user", "test_password", 403),
    ("wrong_user", "wrong_password", 403)
])
def test_incorrect_login(test_user, client, username, password, status_code):
    response = client.post("/users/login", data={
        "username": username,
        "password": password
    })
    assert response.status_code == status_code


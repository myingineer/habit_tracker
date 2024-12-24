from app.Schemas import habits_schemas

# Testing the get_all_habits route
def test_get_all_habits(authorized_client, test_habits):
    response = authorized_client.get("/habits")
    assert response.status_code == 200
    assert len(response.json()) == len(test_habits)

# Testing get_all_habits route without authorization
def test_unauthorized_get_all_habits(client, test_habits):
    response = client.get("/habits")
    assert response.status_code == 401

# Testing the get_a_habit route withouth authorization
def test_unauthorized_get_a_habit(client, test_habits):
    response = client.get(f"/habits/{test_habits[0].habit_id}")
    assert response.status_code == 401

# Testing a non existent habit with authorization
def test_get_non_existent_habit(authorized_client, test_habits):
    response = authorized_client.get("/habits/100")
    assert response.status_code == 404

# Testing the get_a_habit route with authorization
def test_get_a_habit(authorized_client, test_habits):
    response = authorized_client.get(f"/habits/{test_habits[0].habit_id}")
    habit = habits_schemas.Habit(**response.json())
    assert response.status_code == 200
    assert habit.habit == test_habits[0].habit

# Testing the create_habit route with authorization
def test_create_habit(authorized_client, test_user):
    habit_data = {
        "habit": "Test Habit 3",
        "description": "Test Description 3",
        "periodicity": "daily",
        "user_id": test_user["user_id"]
    }
    response = authorized_client.post("/habits", json=habit_data)
    habit = habits_schemas.Habit(**response.json())
    assert response.status_code == 201
    assert habit.habit == habit_data["habit"]
    assert habit.user_id == test_user["user_id"]

# Testing the create habit without a valid periodicity with authorization
def test_create_habit_with_invalid_periodicity(authorized_client, test_user):
    # Habit data with invalid periodicity
    habit_data = {
        "habit": "Test Habit Invalid Periodicity",
        "description": "Test Description",
        "periodicity": "invalid_periodicity",  # Invalid periodicity
        "user_id": test_user["user_id"]
    }
    
    response = authorized_client.post("/habits", json=habit_data)

    assert response.status_code == 422

# Testing deleting a habit with authorization
def test_delete_habit(authorized_client, test_habits):
    response = authorized_client.delete(f"/habits/{test_habits[0].habit_id}")
    assert response.status_code == 204

# Testing deleting a non existent habit with authorization
def test_delete_non_existent_habit(authorized_client):
    response = authorized_client.delete("/habits/100")
    assert response.status_code == 404

# Testing updating a habit with authorization
def test_update_habit(authorized_client, test_habits):
    habit_data = {
        "description": "Test Description Updated",
        "user_id": test_habits[0].user_id
    }
    response = authorized_client.patch(f"/habits/{test_habits[0].habit_id}", json=habit_data)
    habit = habits_schemas.Habit(**response.json())
    assert response.status_code == 200
    assert habit.description == habit_data["description"]
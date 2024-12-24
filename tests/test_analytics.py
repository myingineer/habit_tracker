# Test updating the streak of an existing habit with authorization
def test_update_habit_streak(authorized_client, test_habits):
    response = authorized_client.post(f"/analytics/streak/update", json={
        "habit_id": test_habits[0].habit_id
    })
    assert response.status_code == 200

# Test updating the streak of an exisiting habit without authorization
def test_update_habit_streak_unauthorized(client, test_habits):
    response = client.post(f"/analytics/streak/update", json={
        "habit_id": test_habits[0].habit_id
    })
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

# Test updating the streak of a non existent habit with authorization
def test_update_non_existent_habit_streak(authorized_client):
    response = authorized_client.post("/analytics/streak/update", json={
        "habit_id": 100
    })
    assert response.status_code == 404

# Test updating the streak of a habit with a non existent habit_id with authorization
def test_update_habit_streak_invalid_habit_id(authorized_client):
    response = authorized_client.post("/analytics/streak/update", json={
        "habit_id": 100
    })
    assert response.status_code == 404
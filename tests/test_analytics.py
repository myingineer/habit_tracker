from app.Schemas import analytics_schema

# Testing get all analytics data with authorization
def test_get_all_analytics_data(authorized_client, test_analytics):
    response = authorized_client.get("/analytics")
    assert len(response.json()) == len(test_analytics)
    assert response.status_code == 200

# Testing get all analytics data without authorization
def test_unauthorized_get_all_analytics_data(client, test_analytics):
    response = client.get("/analytics")
    assert response.status_code == 401

# Testing get a single analytics data with authorization
def test_get_analytics_data(authorized_client, test_analytics):
    response = authorized_client.get(f"/analytics/{test_analytics[0].habit_id}")
    analytic_data = analytics_schema.AnalyticResponse(**response.json())
    assert analytic_data.habit_id == test_analytics[0].habit_id
    assert response.status_code == 200

# Testing get a single analytics data without authorization
def test_unauthorized_get_analytics_data(client, test_analytics):
    response = client.get(f"/analytics/{test_analytics[0].habit_id}")
    assert response.status_code == 401

# Test updating the streak of an existing habit with authorization
def test_update_habit_streak(authorized_client, test_analytics):
    response = authorized_client.post(f"/analytics/streak/update", json={
        "habit_id": test_analytics[0].habit_id
    })
    assert response.status_code == 200

# Test updating the streak of an exisiting habit without authorization
def test_update_habit_streak_unauthorized(client, test_analytics):
    response = client.post(f"/analytics/streak/update", json={
        "habit_id": test_analytics[0].habit_id
    })
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}
import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# Arrange-Act-Assert (AAA) pattern is used in all tests

def test_get_activities():
    # Arrange: (nothing to arrange for GET)
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]

def test_signup_for_activity():
    # Arrange
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert f"Signed up {email}" in data["message"]
    # Check participant is added
    get_resp = client.get("/activities")
    assert email in get_resp.json()[activity]["participants"]

def test_signup_duplicate():
    # Arrange
    email = "duplicate@mergington.edu"
    activity = "Programming Class"
    # Act
    client.post(f"/activities/{activity}/signup?email={email}")
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    # This will fail until backend prevents duplicates
    assert response.status_code != 200  # Should be 409 or similar when fixed

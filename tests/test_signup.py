"""Tests for the POST /activities/{activity_name}/signup endpoint."""


def test_signup_new_participant(client):
    """Test signing up a new participant to an activity."""
    response = client.post(
        "/activities/Chess Club/signup?email=newstudent@example.com"
    )
    assert response.status_code == 200
    data = response.json()
    assert "Signed up" in data["message"]
    assert "newstudent@example.com" in data["message"]


def test_signup_adds_participant_to_activity(client):
    """Test that signup actually adds the participant to the activity."""
    client.post("/activities/Chess Club/signup?email=test@example.com")
    
    response = client.get("/activities")
    participants = response.json()["Chess Club"]["participants"]
    assert "test@example.com" in participants


def test_signup_nonexistent_activity(client):
    """Test signup fails for non-existent activity."""
    response = client.post(
        "/activities/Fake Club/signup?email=test@example.com"
    )
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_signup_duplicate_participant(client):
    """Test that signing up the same student twice fails."""
    email = "michael@mergington.edu"
    
    # First signup for someone already registered
    response = client.post(
        f"/activities/Chess Club/signup?email={email}"
    )
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_multiple_activities(client):
    """Test that a student can sign up for multiple activities."""
    email = "versatile@example.com"
    
    response1 = client.post(f"/activities/Chess Club/signup?email={email}")
    assert response1.status_code == 200
    
    response2 = client.post(f"/activities/Programming Class/signup?email={email}")
    assert response2.status_code == 200
    
    # Verify signed up for both
    activities = client.get("/activities").json()
    assert email in activities["Chess Club"]["participants"]
    assert email in activities["Programming Class"]["participants"]


def test_signup_increments_participant_count(client):
    """Test that signup increases the participant count."""
    response_before = client.get("/activities")
    count_before = len(response_before.json()["Chess Club"]["participants"])
    
    client.post("/activities/Chess Club/signup?email=counter@example.com")
    
    response_after = client.get("/activities")
    count_after = len(response_after.json()["Chess Club"]["participants"])
    
    assert count_after == count_before + 1

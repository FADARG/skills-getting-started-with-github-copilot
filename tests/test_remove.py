"""Tests for the DELETE /activities/{activity_name}/participants endpoint."""


def test_remove_participant(client):
    """Test removing a participant from an activity."""
    email = "michael@mergington.edu"
    
    response = client.delete(
        f"/activities/Chess Club/participants?email={email}"
    )
    assert response.status_code == 200
    assert "Removed" in response.json()["message"]


def test_remove_updates_activity(client):
    """Test that removal actually updates the activity."""
    email = "michael@mergington.edu"
    
    # Verify participant is there
    activities_before = client.get("/activities").json()
    assert email in activities_before["Chess Club"]["participants"]
    
    # Remove participant
    client.delete(f"/activities/Chess Club/participants?email={email}")
    
    # Verify removed
    activities_after = client.get("/activities").json()
    assert email not in activities_after["Chess Club"]["participants"]


def test_remove_nonexistent_activity(client):
    """Test removing from non-existent activity fails."""
    response = client.delete(
        "/activities/Fake Club/participants?email=test@example.com"
    )
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_remove_nonexistent_participant(client):
    """Test removing non-existent participant from activity fails."""
    response = client.delete(
        "/activities/Chess Club/participants?email=notamember@example.com"
    )
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]


def test_remove_then_readd(client):
    """Test that a removed participant can re-signup."""
    email = "michael@mergington.edu"
    
    # Remove
    client.delete(f"/activities/Chess Club/participants?email={email}")
    
    # Try to re-add
    response = client.post(f"/activities/Chess Club/signup?email={email}")
    assert response.status_code == 200
    
    # Verify re-added
    activities = client.get("/activities").json()
    assert email in activities["Chess Club"]["participants"]


def test_remove_decrements_participant_count(client):
    """Test that removal decreases the participant count."""
    response_before = client.get("/activities")
    count_before = len(response_before.json()["Chess Club"]["participants"])
    
    client.delete("/activities/Chess Club/participants?email=michael@mergington.edu")
    
    response_after = client.get("/activities")
    count_after = len(response_after.json()["Chess Club"]["participants"])
    
    assert count_after == count_before - 1

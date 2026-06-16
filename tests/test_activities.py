"""Tests for the GET /activities endpoint."""


def test_get_activities_returns_all(client):
    """Test that GET /activities returns all activities."""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data


def test_activity_structure(client):
    """Test that each activity has required fields."""
    response = client.get("/activities")
    data = response.json()
    
    activity = data["Chess Club"]
    assert "description" in activity
    assert "schedule" in activity
    assert "max_participants" in activity
    assert "participants" in activity
    assert isinstance(activity["participants"], list)


def test_activities_have_participants(client):
    """Test that activities include current participant data."""
    response = client.get("/activities")
    data = response.json()
    
    chess_participants = data["Chess Club"]["participants"]
    assert "michael@mergington.edu" in chess_participants
    assert "daniel@mergington.edu" in chess_participants


def test_all_activities_returned(client):
    """Test that all 9 activities are returned."""
    response = client.get("/activities")
    data = response.json()
    assert len(data) == 9
    
    expected_activities = [
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Soccer Team",
        "Basketball Club",
        "Art Club",
        "Drama Club",
        "Science Club",
        "Debate Team"
    ]
    for activity in expected_activities:
        assert activity in data

from fastapi.testclient import TestClient

from oceanic_os.api import app

client = TestClient(app)


def test_bulk_create_identities() -> None:
    """Test creating multiple identities in bulk."""
    payload = {
        "identities": [
            {"id": "bulk1", "name": "Bulk User 1", "email": "bulk1@example.com"},
            {"id": "bulk2", "name": "Bulk User 2", "email": "bulk2@example.com"},
            {"id": "bulk3", "name": "Bulk User 3", "email": "bulk3@example.com"},
        ]
    }

    response = client.post("/identities/bulk", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["created"] == 3
    assert data["failed"] == 0
    assert len(data["identities"]) == 3


def test_bulk_create_with_duplicates() -> None:
    """Test bulk create handles duplicates gracefully."""
    # Create one first
    client.post("/identity", json={"id": "dup1", "name": "Existing", "email": "existing@example.com"})

    payload = {
        "identities": [
            {"id": "dup1", "name": "Duplicate", "email": "dup@example.com"},  # Already exists
            {"id": "new1", "name": "New User", "email": "new@example.com"},  # New
        ]
    }

    response = client.post("/identities/bulk", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["created"] == 1
    assert data["failed"] == 1
    assert len(data["errors"]) == 1


def test_stats_endpoint() -> None:
    """Test the stats endpoint returns system information."""
    response = client.get("/stats")
    assert response.status_code == 200
    data = response.json()
    
    assert "identities_count" in data
    assert "events_count" in data
    assert "recent_events" in data
    assert "uptime" in data
    assert data["identities_count"] >= 0
    assert data["events_count"] >= 0
    assert isinstance(data["recent_events"], list)


def test_stats_reflect_operations() -> None:
    """Test that stats update after operations."""
    # Get initial stats
    initial = client.get("/stats").json()
    initial_count = initial["identities_count"]

    # Create a new identity
    client.post("/identity", json={"id": "stats-test", "name": "Stats Test", "email": "stats@example.com"})

    # Get updated stats
    updated = client.get("/stats").json()
    assert updated["identities_count"] == initial_count + 1

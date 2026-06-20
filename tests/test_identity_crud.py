from fastapi.testclient import TestClient

from oceanic_os.api import app

client = TestClient(app)


def test_update_identity() -> None:
    """Test updating an existing identity."""
    # Create an identity
    create_payload = {"id": "user-update", "name": "Original", "email": "orig@example.com"}
    client.post("/identity", json=create_payload)

    # Update it
    update_payload = {"id": "user-update", "name": "Updated", "email": "updated@example.com"}
    response = client.put("/identity/user-update", json=update_payload)
    assert response.status_code == 200
    assert response.json()["identity"]["name"] == "Updated"

    # Verify the update
    get_response = client.get("/identity/user-update")
    assert get_response.json()["name"] == "Updated"


def test_delete_identity() -> None:
    """Test deleting an identity."""
    # Create an identity
    create_payload = {"id": "user-delete", "name": "ToDelete", "email": "delete@example.com"}
    client.post("/identity", json=create_payload)

    # Delete it
    response = client.delete("/identity/user-delete")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

    # Verify it's gone
    get_response = client.get("/identity/user-delete")
    assert get_response.status_code == 404


def test_search_identities() -> None:
    """Test searching identities by name and email."""
    # Create test identities
    client.post("/identity", json={"id": "alice", "name": "Alice Wonder", "email": "alice@example.com"})
    client.post("/identity", json={"id": "bob", "name": "Bob Smith", "email": "bob@example.com"})

    # Search by name
    response = client.get("/identities?search=alice")
    assert len(response.json()) >= 1
    assert any(i["id"] == "alice" for i in response.json())

    # Search by email
    response = client.get("/identities?search=bob@")
    assert any(i["id"] == "bob" for i in response.json())

    # Search with no results
    response = client.get("/identities?search=nonexistent")
    assert len(response.json()) == 0


def test_identity_conflict() -> None:
    """Test that creating duplicate identity fails."""
    payload = {"id": "dup", "name": "Duplicate", "email": "dup@example.com"}
    client.post("/identity", json=payload)

    # Try to create again
    response = client.post("/identity", json=payload)
    assert response.status_code == 409
    assert "already exists" in response.json()["detail"]


def test_update_nonexistent_identity() -> None:
    """Test updating a non-existent identity fails."""
    payload = {"id": "nonexistent", "name": "Test", "email": "test@example.com"}
    response = client.put("/identity/nonexistent", json=payload)
    assert response.status_code == 404

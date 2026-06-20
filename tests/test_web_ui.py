from fastapi.testclient import TestClient

from oceanic_os.api import app

client = TestClient(app)


def test_root_redirects_to_static_index() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "Oceanic-OS Dashboard" in response.text


def test_create_identity_updates_identities() -> None:
    payload = {"id": "user-web", "name": "Web User", "email": "web@example.com"}
    response = client.post("/identity", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

    identities_response = client.get("/identities")
    assert identities_response.status_code == 200
    data = identities_response.json()["data"]
    assert any(identity["id"] == "user-web" for identity in data)

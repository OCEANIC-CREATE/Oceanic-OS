from fastapi.testclient import TestClient

from oceanic_os.api import app

client = TestClient(app)


def test_memory_endpoint_and_record() -> None:
    response = client.get("/memory")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

    payload = {"event": "test_event", "payload": {"value": 1}}
    post_response = client.post("/memory", json=payload)
    assert post_response.status_code == 200
    assert post_response.json()["status"] == "ok"
    assert post_response.json()["memory"]["event"] == "test_event"

    timeline = client.get("/memory")
    assert any(item["event"] == "test_event" for item in timeline.json())

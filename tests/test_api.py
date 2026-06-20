import json
import threading
import time
from http.server import HTTPServer, SimpleHTTPRequestHandler

import pytest
from fastapi.testclient import TestClient

from oceanic_os.api import app

client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_dashboard_endpoint() -> None:
    response = client.get("/dashboard")
    assert response.status_code == 200
    assert "identities" in response.json()
    assert "events" in response.json()


def test_create_identity_endpoint() -> None:
    payload = {"id": "user-test", "name": "Test User", "email": "test@example.com"}
    response = client.post("/identity", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["identity"]["id"] == payload["id"]


def test_web_static_root_serves_index() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Oceanic-OS Dashboard" in response.text

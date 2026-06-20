import pytest

from oceanic_os import Identity, IdentityStore, MemoryStore, Dashboard


def test_identity_store_add_and_get() -> None:
    store = IdentityStore()
    identity = Identity(id="user1", name="Alice", email="alice@example.com")
    store.add(identity)

    assert store.get("user1") == identity
    assert store.list() == [identity]


def test_memory_store_record_and_timeline() -> None:
    memory = MemoryStore()
    memory.record("start", {"data": 1})
    memory.record("stop", {"data": 2})

    timeline = memory.timeline()
    assert len(timeline) == 2
    assert timeline[0]["event"] == "start"
    assert timeline[1]["event"] == "stop"


def test_dashboard_render() -> None:
    identity_store = IdentityStore()
    memory_store = MemoryStore()
    identity_store.add(Identity(id="user1", name="Alice", email="alice@example.com"))
    memory_store.record("start", {"data": 1})

    dashboard = Dashboard(identity_store, memory_store)
    output = dashboard.render()

    assert "Oceanic-OS Dashboard" in output
    assert "Identities: 1" in output
    assert "Memory events: 1" in output

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from .dashboard import Dashboard
from .identity import Identity, IdentityStore
from .memory import MemoryStore

app = FastAPI(
    title="Oceanic-OS API",
    description="Full-stack prototype for identity, memory, dashboard, and ecosystem.",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

identity_store = IdentityStore()
memory_store = MemoryStore()

identity_store.add(Identity(id="user1", name="Alice", email="alice@example.com"))
memory_store.record("seed", {"source": "startup"})
app.mount("/static", StaticFiles(directory="web"), name="static")


class IdentityPayload(BaseModel):
    id: str
    name: str
    email: str

class MemoryPayload(BaseModel):
    event: str
    payload: dict[str, object] = {}

@app.get("/health", tags=["Core"])
def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}


@app.get("/dashboard", tags=["Dashboard"])
def dashboard() -> dict[str, object]:
    """Get dashboard summary with identity and event counts."""
    return Dashboard(identity_store, memory_store).summary()


@app.get("/identities", tags=["Identities"])
def get_identities(search: str = "") -> list[dict[str, str]]:
    """List identities, optionally filtered by name or email."""
    identities = identity_store.list()
    if search:
        search_lower = search.lower()
        identities = [
            i for i in identities
            if search_lower in i.name.lower() or search_lower in i.email.lower()
        ]
    return [identity.__dict__ for identity in identities]


@app.get("/identity/{identity_id}", tags=["Identities"])
def get_identity(identity_id: str) -> dict[str, str]:
    """Get a single identity by ID."""
    identity = identity_store.get(identity_id)
    if not identity:
        raise HTTPException(status_code=404, detail="Identity not found")
    return identity.__dict__


@app.post("/identity", tags=["Identities"])
def create_identity(identity: IdentityPayload) -> dict[str, object]:
    """Create a new identity."""
    if identity_store.get(identity.id):
        raise HTTPException(status_code=409, detail="Identity already exists")
    new_identity = Identity(**identity.model_dump())
    identity_store.add(new_identity)
    memory_store.record("identity_added", new_identity.__dict__)
    return {"status": "ok", "identity": new_identity.__dict__}


@app.put("/identity/{identity_id}", tags=["Identities"])
def update_identity(identity_id: str, identity: IdentityPayload) -> dict[str, object]:
    """Update an existing identity."""
    existing = identity_store.get(identity_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Identity not found")
    updated_identity = Identity(**identity.model_dump())
    identity_store.add(updated_identity)
    memory_store.record("identity_updated", updated_identity.__dict__)
    return {"status": "ok", "identity": updated_identity.__dict__}


@app.delete("/identity/{identity_id}", tags=["Identities"])
def delete_identity(identity_id: str) -> dict[str, object]:
    """Delete an identity."""
    existing = identity_store.get(identity_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Identity not found")
    identity_store.delete(identity_id)
    memory_store.record("identity_deleted", {"id": identity_id})
    return {"status": "ok", "message": f"Identity {identity_id} deleted"}


@app.get("/memory", tags=["Memory"])
def get_memory() -> list[dict[str, object]]:
    """Get the memory timeline of all recorded events."""
    return memory_store.timeline()


@app.post("/memory", tags=["Memory"])
def record_memory(payload: MemoryPayload) -> dict[str, object]:
    """Record a new memory event."""
    memory_store.record(payload.event, payload.payload)
    return {"status": "ok", "memory": {"event": payload.event, "payload": payload.payload}}


@app.get("/")
def root() -> RedirectResponse:
    return RedirectResponse(url="/static/index.html")

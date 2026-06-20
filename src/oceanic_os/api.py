from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from .dashboard import Dashboard
from .identity import Identity, IdentityStore
from .memory import MemoryStore

app = FastAPI(
    title="Oceanic-OS",
    description="One-drop full-stack prototype for identity, memory, dashboard, and ecosystem.",
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

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/dashboard")
def dashboard() -> dict[str, object]:
    return Dashboard(identity_store, memory_store).summary()


@app.get("/identities")
def get_identities() -> list[dict[str, str]]:
    return [identity.__dict__ for identity in identity_store.list()]


@app.post("/identity")
def create_identity(identity: IdentityPayload) -> dict[str, object]:
    new_identity = Identity(**identity.dict())
    identity_store.add(new_identity)
    memory_store.record("identity_added", new_identity.__dict__)
    return {"status": "ok", "identity": new_identity.__dict__}


@app.get("/")
def root() -> RedirectResponse:
    return RedirectResponse(url="/static/index.html")

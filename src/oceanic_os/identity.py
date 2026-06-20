from dataclasses import dataclass
from typing import Dict

@dataclass
class Identity:
    id: str
    name: str
    email: str

class IdentityStore:
    def __init__(self) -> None:
        self._store: Dict[str, Identity] = {}

    def add(self, identity: Identity) -> None:
        self._store[identity.id] = identity

    def get(self, identity_id: str) -> Identity | None:
        return self._store.get(identity_id)

    def list(self) -> list[Identity]:
        return list(self._store.values())

    def delete(self, identity_id: str) -> None:
        if identity_id in self._store:
            del self._store[identity_id]

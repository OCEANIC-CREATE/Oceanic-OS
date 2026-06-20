from datetime import datetime, timezone
from typing import Any

class MemoryStore:
    def __init__(self) -> None:
        self._history: list[dict[str, Any]] = []

    def record(self, event: str, payload: Any) -> None:
        self._history.append({
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "event": event,
            "payload": payload,
        })

    def timeline(self) -> list[dict[str, Any]]:
        return list(self._history)

    def last(self, n: int = 1) -> list[dict[str, Any]]:
        return self._history[-n:]

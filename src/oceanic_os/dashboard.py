from typing import Any

class Dashboard:
    def __init__(self, identity_store: Any, memory_store: Any) -> None:
        self.identity_store = identity_store
        self.memory_store = memory_store

    def summary(self) -> dict[str, Any]:
        return {
            "identities": len(self.identity_store.list()),
            "events": len(self.memory_store.timeline()),
            "recent": self.memory_store.last(3),
        }

    def render(self) -> str:
        summary = self.summary()
        lines = [
            "Oceanic-OS Dashboard",
            "===================",
            f"Identities: {summary['identities']}",
            f"Memory events: {summary['events']}",
            "Recent events:",
        ]
        for item in summary["recent"]:
            lines.append(f"- {item['timestamp']} {item['event']}")
        return "\n".join(lines)

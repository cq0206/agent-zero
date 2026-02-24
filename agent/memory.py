from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class Memory:
    """
    v0.1 minimal memory:
    - store events (tool calls, outputs, key notes)
    - allow summarization later
    """
    events: List[Dict[str, Any]] = field(default_factory=list)

    def add_event(self, kind: str, payload: Dict[str, Any]):
        self.events.append({"kind": kind, "payload": payload})

    def snapshot_text(self, max_events: int = 20) -> str:
        # Minimal readable snapshot for planner/judge context
        tail = self.events[-max_events:]
        lines = []
        for e in tail:
            kind = e.get("kind")
            payload = e.get("payload", {})
            lines.append(f"- {kind}: {payload}")
        return "\n".join(lines) if lines else "None"
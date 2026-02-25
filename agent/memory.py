import json
import os
from dataclasses import dataclass, field
from typing import Any, Dict, List

MEMORY_FILE = "memory.json"


@dataclass
class Memory:

    events: List[Dict[str, Any]] = field(default_factory=list)
    summary: str = ""

    def __post_init__(self):
        self._load()

    # ========= Load =========

    def _load(self):

        if os.path.exists(MEMORY_FILE):

            with open(MEMORY_FILE, "r") as f:

                data = json.load(f)

                self.events = data.get("events", [])

                self.summary = data.get("summary", "")

    # ========= Save =========

    def save(self):

        with open(MEMORY_FILE, "w") as f:

            json.dump(
                {
                    "events": self.events,
                    "summary": self.summary,
                },
                f,
                indent=2,
            )

    # ========= Add Event =========

    def add_event(self, kind: str, payload: Dict[str, Any]):

        self.events.append(
            {
                "kind": kind,
                "payload": payload,
            }
        )

    # ========= Snapshot =========

    def snapshot_text(self):

        text = f"""
Summary:
{self.summary}

Recent events:
{self.events[-10:]}
"""

        return text

    # ========= Update Summary =========

    def update_summary(self, llm):

        if not self.events:
            return

        prompt = f"""
Summarize these agent events into key learnings:

{self.events[-20:]}

Return concise bullet points.
"""

        summary = llm.chat(
            [
                {"role": "system", "content": "You summarize agent memory."},
                {"role": "user", "content": prompt},
            ]
        )

        self.summary = summary

        self.save()
import json
import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from agent.vector_store import VectorStore
from core.embeddings import Embeddings

MEMORY_FILE = "memory.json"


@dataclass
class Memory:
    """
    Day5 memory:
    - short-term events (in-memory + persisted to memory.json)
    - long-term summary (string)
    - vector memory (persistent JSON store)
    """

    events: List[Dict[str, Any]] = field(default_factory=list)
    summary: str = ""
    vector_store: Optional[VectorStore] = None

    def __post_init__(self):
        self._load()

    def _load(self):
        if os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.events = data.get("events", [])
            self.summary = data.get("summary", "")

    def save(self):
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "events": self.events,
                    "summary": self.summary,
                },
                f,
                ensure_ascii=False,
                indent=2,
            )

    def init_vector(self):
        if self.vector_store is None:
            emb = Embeddings()
            self.vector_store = VectorStore(embeddings=emb)

    def add_event(self, kind: str, payload: Dict[str, Any]):
        self.events.append({"kind": kind, "payload": payload})

    def snapshot_text(self, max_events: int = 20) -> str:
        tail = self.events[-max_events:]
        lines = []
        for e in tail:
            lines.append(f"- {e.get('kind')}: {e.get('payload')}")
        return (
            "Summary:\n"
            f"{self.summary or 'None'}\n\n"
            "Recent events:\n"
            f"{chr(10).join(lines) if lines else 'None'}"
        )

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

    def remember(self, text: str, meta: Optional[Dict[str, Any]] = None) -> str:
        """
        Add a long-term memory snippet into vector store.
        Keep this concise and fact-like for better retrieval.
        """
        self.init_vector()
        assert self.vector_store is not None
        return self.vector_store.add(text=text, meta=meta or {})

    def recall(self, query: str, top_k: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Retrieve top_k most relevant memories for a query.
        Returns: [{score, id, text, meta}, ...]
        """
        self.init_vector()
        assert self.vector_store is not None

        k = top_k or int(os.getenv("VECTOR_TOP_K", "5"))
        hits = self.vector_store.search(query=query, top_k=k)

        out: List[Dict[str, Any]] = []
        for score, item in hits:
            out.append(
                {
                    "score": float(score),
                    "id": item.id,
                    "text": item.text,
                    "meta": item.meta,
                }
            )
        return out

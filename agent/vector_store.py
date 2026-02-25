import json
import math
import os
import time
from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional, Tuple

from core.embeddings import Embeddings


def _cosine(a: List[float], b: List[float]) -> float:
    if not a or not b or len(a) != len(b):
        return 0.0
    dot = 0.0
    na = 0.0
    nb = 0.0
    for x, y in zip(a, b):
        dot += x * y
        na += x * x
        nb += y * y
    if na == 0.0 or nb == 0.0:
        return 0.0
    return dot / (math.sqrt(na) * math.sqrt(nb))


@dataclass
class VectorItem:
    id: str
    text: str
    embedding: List[float]
    meta: Dict[str, Any]
    created_at: float


class VectorStore:
    """
    Minimal persistent vector store:
    - stores (text, embedding, meta) in a JSON file
    - supports similarity search by cosine
    """

    def __init__(self, embeddings: Embeddings, path: Optional[str] = None):
        self.emb = embeddings
        self.path = path or os.getenv("VECTOR_STORE_PATH", "memory_vectors.json")
        self.items: List[VectorItem] = []
        self._load()

    def _load(self):
        if os.path.exists(self.path):
            with open(self.path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.items = [VectorItem(**x) for x in data.get("items", [])]
        else:
            self.items = []

    def save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump({"items": [asdict(x) for x in self.items]}, f, ensure_ascii=False, indent=2)

    def add(self, text: str, meta: Optional[Dict[str, Any]] = None, item_id: Optional[str] = None) -> str:
        text = (text or "").strip()
        if not text:
            return ""

        emb = self.emb.embed(text)
        if not emb:
            return ""

        item_id = item_id or f"mem_{int(time.time() * 1000)}"
        meta = meta or {}

        self.items.append(
            VectorItem(
                id=item_id,
                text=text,
                embedding=emb,
                meta=meta,
                created_at=time.time(),
            )
        )
        self.save()
        return item_id

    def search(self, query: str, top_k: int = 5) -> List[Tuple[float, VectorItem]]:
        q = (query or "").strip()
        if not q or not self.items:
            return []

        q_emb = self.emb.embed(q)
        if not q_emb:
            return []

        scored: List[Tuple[float, VectorItem]] = []
        for it in self.items:
            s = _cosine(q_emb, it.embedding)
            scored.append((s, it))

        scored.sort(key=lambda x: x[0], reverse=True)
        return scored[: max(1, top_k)]

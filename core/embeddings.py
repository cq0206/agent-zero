import os
from typing import List

from openai import OpenAI


class Embeddings:
    """
    Minimal OpenAI-compatible embeddings wrapper.
    Uses same OPENAI_API_KEY / OPENAI_BASE_URL if you set them.
    """

    def __init__(
        self,
        model: str | None = None,
        api_key: str | None = None,
        base_url: str | None = None,
    ):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise RuntimeError("Missing OPENAI_API_KEY for embeddings.")

        self.base_url = base_url or os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
        self.model = model or os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-small")

        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

    def embed(self, text: str) -> List[float]:
        text = (text or "").strip()
        if not text:
            return []
        resp = self.client.embeddings.create(
            model=self.model,
            input=text,
        )
        return resp.data[0].embedding

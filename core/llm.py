import os
from openai import OpenAI


class LLM:
    """
    OpenAI-compatible LLM wrapper with configurable base_url.

    Supports:
    - OpenAI
    - Azure OpenAI
    - vLLM
    - OpenRouter
    - Gemini (OpenAI-compatible endpoint)
    - Any OpenAI-compatible API
    """

    def __init__(
        self,
        model: str | None = None,
        api_key: str | None = None,
        base_url: str | None = None,
    ):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")

        if not self.api_key:
            raise RuntimeError("Missing OPENAI_API_KEY")

        self.base_url = base_url or os.getenv(
            "OPENAI_BASE_URL",
            "https://api.openai.com/v1",
        )

        self.model = model or os.getenv(
            "OPENAI_MODEL",
            "gpt-4o-mini",
        )

        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
            timeout=60.0,
        )

    def chat(
        self,
        messages: list[dict],
        temperature: float = 0,
        max_tokens: int | None = None,
    ) -> str:

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        return response.choices[0].message.content or ""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict


class Tool(ABC):
    name: str
    description: str

    @abstractmethod
    def run(self, **kwargs) -> Any:
        raise NotImplementedError

    def spec(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "params": {},
        }


class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, Tool] = {}

    def register(self, tool: Tool):
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool | None:
        return self._tools.get(name)

    def list(self) -> list[str]:
        return sorted(self._tools.keys())

    def run(self, name: str | None, args: dict | None = None) -> Any:
        tool = self.get(name or "")
        if not tool:
            return f"[ERROR] Tool not found: {name}"
        return tool.run(**(args or {}))

    def specs(self) -> list[dict]:
        return [tool.spec() for tool in self._tools.values()]

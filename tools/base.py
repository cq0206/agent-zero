from abc import ABC, abstractmethod
from typing import Any, Dict


class Tool(ABC):
    name: str
    description: str

    @abstractmethod
    def run(self, **kwargs) -> Any:
        raise NotImplementedError


class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, Tool] = {}

    def register(self, tool: Tool):
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool | None:
        return self._tools.get(name)

    def list(self) -> list[str]:
        return sorted(self._tools.keys())
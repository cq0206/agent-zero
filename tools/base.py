from __future__ import annotations

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
    
    def specs(self) -> list[dict]:
        specs = []
        for tool in self._tools.values():
            # v0.1: 只给 query 参数的示例
            # 后面可以做成每个 tool 自己暴露 schema
            params = {"query": "string"} if tool.name == "search_web" else {}
            specs.append({
                "name": tool.name,
                "description": tool.description,
                "params": params
            })
        return specs

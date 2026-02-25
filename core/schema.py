from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field


class Task(BaseModel):
    id: str
    description: str
    expected_output: str
    tool: Optional[str] = None
    args: Dict[str, Any] = Field(default_factory=dict)


class Plan(BaseModel):
    tasks: List[Task]


class JudgeResult(BaseModel):
    decision: Literal["SUFFICIENT", "REPLAN"]
    missing: List[str] = Field(default_factory=list)

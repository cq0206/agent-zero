from pydantic import BaseModel, Field
from typing import List, Literal, Optional


class Task(BaseModel):
    id: str = Field(..., description="Unique task id, e.g. t1, t2")
    description: str = Field(..., description="What to do")
    expected_output: str = Field(..., description="What result should look like")
    tool: Optional[str] = Field(
        default=None,
        description="Optional tool name if this task should use a tool, e.g. search_web",
    )


class Plan(BaseModel):
    tasks: List[Task]


JudgeDecision = Literal["SUFFICIENT", "REPLAN"]


class JudgeResult(BaseModel):
    decision: JudgeDecision
    missing: List[str] = Field(default_factory=list)
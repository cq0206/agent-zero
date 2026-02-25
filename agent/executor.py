from dataclasses import dataclass
from typing import Any, Dict, List

from agent.recovery import RetryConfig, retry_llm_call
from core.llm import LLM
from core.schema import Plan, Task
from tools.base import ToolRegistry
from agent.memory import Memory


@dataclass
class StepResult:
    task_id: str
    description: str
    output: str


class Executor:
    """
    Executes a Plan.
    Strategy (v0.1):
    - If task.tool is set: call that tool with a simple argument
    - Else: ask LLM to produce the output directly
    """

    def __init__(self, llm: LLM, tools: ToolRegistry, memory: Memory):
        self.llm = llm
        self.tools = tools
        self.memory = memory

    def _execute_task_with_llm(self, task: Task) -> str:
        prompt = f"""You are an analyst executing a task.

Task: {task.description}
Expected output: {task.expected_output}

Return a concise result that matches the expected output.
"""
        return self.llm.chat(
            [{"role": "system", "content": "You are a careful analyst."},
             {"role": "user", "content": prompt}],
            temperature=0,
        )

    def _execute_task_with_tool(self, task: Task) -> str:
        args = dict(task.args or {})
        if not args:
            # Compatibility fallback for old plans that omitted args.
            args = {"query": task.description}
        out = retry_llm_call(
            lambda: self.tools.run(task.tool, args),
            RetryConfig(max_retries=2),
        )
        return str(out)

    def execute(self, plan: Plan) -> List[StepResult]:
        results: List[StepResult] = []

        for task in plan.tasks:
            if task.tool:
                output = self._execute_task_with_tool(task)
                self.memory.add_event("tool_call", {"tool": task.tool, "task_id": task.id, "desc": task.description})
            else:
                output = self._execute_task_with_llm(task)

            self.memory.add_event("task_done", {"task_id": task.id, "output_preview": output[:200]})
            results.append(StepResult(task_id=task.id, description=task.description, output=output))

        return results

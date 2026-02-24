from typing import List
from agent.planner import Planner
from agent.executor import Executor, StepResult
from agent.judge import Judge
from agent.memory import Memory


class AgentRuntime:
    def __init__(self, planner: Planner, executor: Executor, judge: Judge, memory: Memory):
        self.planner = planner
        self.executor = executor
        self.judge = judge
        self.memory = memory

    def _compile_report(self, goal: str, steps: List[StepResult]) -> str:
        # v0.1: compile deterministically; later can add LLM summarizer
        lines = [f"# Report\n\n## Goal\n{goal}\n\n## Findings\n"]
        for s in steps:
            lines.append(f"### {s.task_id}: {s.description}\n{s.output}\n")
        return "\n".join(lines)

    def run(self, goal: str, max_rounds: int = 3) -> str:
        previous_report = None

        for round_idx in range(max_rounds):
            snapshot = self.memory.snapshot_text()

            plan = self.planner.create(
                goal=goal,
                previous_report=previous_report,
                memory_snapshot=snapshot,
            )

            steps = self.executor.execute(plan)
            report = self._compile_report(goal, steps)

            jr = self.judge.evaluate(goal, report)

            self.memory.add_event("judge", {"decision": jr.decision, "missing": jr.missing})

            if jr.decision == "SUFFICIENT":
                return report

            # Replan: feed report back next round
            previous_report = report

        return previous_report or ""

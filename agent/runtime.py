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
        max_replans = 2
        replan_count = 0

        for round_idx in range(max_rounds):
            snapshot = self.memory.snapshot_text()
            recalled = self.memory.recall(goal, top_k=5)

            plan = self.planner.create(
                goal=goal,
                previous_report=previous_report,
                memory_snapshot=snapshot,
                tool_specs=self.executor.tools.specs(),
                recalled_memories=recalled,
            )

            steps = self.executor.execute(plan)
            report = self._compile_report(goal, steps)
            self.memory.remember(
                text=f"Goal: {goal}\nKey result: {report[:1200]}",
                meta={"type": "report", "goal": goal, "round": round_idx + 1},
            )

            jr = self.judge.evaluate(goal, report)

            self.memory.add_event("judge", {"decision": jr.decision, "missing": jr.missing})

            if jr.decision == "SUFFICIENT":
                self.memory.update_summary(self.planner.llm)

                self.memory.save()

                return report
            else:
                replan_count += 1
                if replan_count > max_replans:
                    print("Recovery: Max replans reached")
                    return report

            # Replan: feed report back next round
            previous_report = report

        return previous_report or ""

import json
import os
import time
from typing import Any, Dict, List

from agent.memory import Memory
from agent.planner import Planner
from core.llm import LLM
from core.schema import Plan
from tools.base import ToolRegistry
from tools.search import SearchWebTool


def score_plan(plan: Plan, allowed_tools: List[str]) -> Dict[str, Any]:
    tasks = plan.tasks
    n = len(tasks)

    has_ids = all(t.id for t in tasks)
    has_expected = all(t.expected_output for t in tasks)
    tool_ok = all((t.tool is None) or (t.tool in allowed_tools) for t in tasks)
    args_ok = all((t.tool is None) or isinstance(t.args, dict) for t in tasks)

    concrete = sum(1 for t in tasks if len(t.description.strip()) >= 12) / max(n, 1)
    verifiable = sum(
        1
        for t in tasks
        if any(
            k in t.expected_output.lower()
            for k in ["bullet", "table", "list", "fields", "compare", "metrics", "decision"]
        )
    ) / max(n, 1)

    valid = bool(n >= 4 and n <= 8 and has_ids and has_expected and tool_ok and args_ok)

    score = 0
    score += 40 if valid else 0
    score += int(30 * concrete)
    score += int(30 * verifiable)

    return {
        "valid": valid,
        "n_tasks": n,
        "tool_ok": tool_ok,
        "args_ok": args_ok,
        "concrete_ratio": round(concrete, 3),
        "verifiable_ratio": round(verifiable, 3),
        "score": score,
    }


def load_goals(path: str) -> List[Dict[str, Any]]:
    goals = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            goals.append(json.loads(line))
    return goals


def main():
    dataset_path = os.getenv("EVAL_DATASET", "eval/datasets/planner_goals.jsonl")
    out_path = os.getenv("EVAL_OUT", "eval/results/planner_eval.jsonl")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    llm = LLM()
    planner = Planner(llm)

    tools = ToolRegistry()
    tools.register(SearchWebTool())
    tool_specs = tools.specs()
    allowed_tools = tools.list()

    memory = Memory()
    snapshot = memory.snapshot_text()

    goals = load_goals(dataset_path)

    with open(out_path, "w", encoding="utf-8") as out:
        for g in goals:
            gid = g["id"]
            goal = g["goal"]

            t0 = time.time()
            try:
                plan = planner.create(
                    goal=goal,
                    previous_report=None,
                    memory_snapshot=snapshot,
                    tool_specs=tool_specs,
                    recalled_memories=[],
                )
                metrics = score_plan(plan, allowed_tools)
                status = "ok"
                err = None
                plan_json = plan.model_dump()
            except Exception as e:
                status = "fail"
                err = str(e)
                metrics = {"valid": False, "score": 0}
                plan_json = None

            dt_ms = int((time.time() - t0) * 1000)

            rec = {
                "id": gid,
                "status": status,
                "latency_ms": dt_ms,
                "metrics": metrics,
                "plan": plan_json,
                "error": err,
            }
            out.write(json.dumps(rec, ensure_ascii=False) + "\n")

            print(f"[{gid}] {status} score={metrics.get('score')} latency={dt_ms}ms")


if __name__ == "__main__":
    main()

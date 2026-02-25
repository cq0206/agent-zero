import json
import os
from typing import Any, Dict, List


def load_records(path: str) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def main():
    in_path = os.getenv("EVAL_OUT", "eval/results/planner_eval.jsonl")
    rows = load_records(in_path)
    if not rows:
        print("No eval records found.")
        return

    total = len(rows)
    ok_rows = [r for r in rows if r.get("status") == "ok"]
    fail_rows = [r for r in rows if r.get("status") != "ok"]
    valid_rows = [r for r in ok_rows if r.get("metrics", {}).get("valid")]

    avg_score = sum(r.get("metrics", {}).get("score", 0) for r in rows) / total
    avg_latency = sum(r.get("latency_ms", 0) for r in rows) / total

    print("=== Planner Eval Summary ===")
    print(f"dataset: {in_path}")
    print(f"total: {total}")
    print(f"ok: {len(ok_rows)}")
    print(f"fail: {len(fail_rows)}")
    print(f"valid_rate: {len(valid_rows) / total:.2%}")
    print(f"avg_score: {avg_score:.2f}")
    print(f"avg_latency_ms: {avg_latency:.1f}")

    print("\n=== Top Failures ===")
    if not fail_rows:
        print("none")
    else:
        for r in fail_rows[:5]:
            print(f"- {r.get('id')}: {r.get('error')}")

    print("\n=== Lowest Scores ===")
    by_score = sorted(rows, key=lambda x: x.get("metrics", {}).get("score", 0))
    for r in by_score[:5]:
        score = r.get("metrics", {}).get("score", 0)
        print(f"- {r.get('id')}: score={score} status={r.get('status')} latency_ms={r.get('latency_ms')}")


if __name__ == "__main__":
    main()

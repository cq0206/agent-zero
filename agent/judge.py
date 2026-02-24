import json
from core.llm import LLM
from core.schema import JudgeResult


JUDGE_SYSTEM = """You are a strict evaluator.

You will receive a draft report.
Decide if it is sufficient for the goal.

Return ONLY valid JSON:
{
  "decision": "SUFFICIENT" | "REPLAN",
  "missing": ["..."]  // if REPLAN, list missing critical elements; else empty list
}

Be strict but practical.
"""


def _strip_code_fences(text: str) -> str:
    t = text.strip()
    if t.startswith("```"):
        t = t.replace("```json", "").replace("```", "").strip()
    return t


class Judge:
    def __init__(self, llm: LLM):
        self.llm = llm

    def evaluate(self, goal: str, report: str) -> JudgeResult:
        user = f"""Goal: {goal}

Draft report:
{report}

Now judge.
"""
        raw = self.llm.chat(
            [{"role": "system", "content": JUDGE_SYSTEM},
             {"role": "user", "content": user}],
            temperature=0,
        )
        raw = _strip_code_fences(raw)
        data = json.loads(raw)
        return JudgeResult.model_validate(data)
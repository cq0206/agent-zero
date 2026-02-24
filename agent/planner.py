import json
from core.llm import LLM
from core.schema import Plan


PLANNER_SYSTEM = """You are an expert agent planner.
Create a step-by-step research plan as VALID JSON matching this schema:

{
  "tasks": [
    {
      "id": "t1",
      "description": "...",
      "expected_output": "...",
      "tool": "search_web" | null
    }
  ]
}

Rules:
- Return ONLY JSON (no markdown, no code fences).
- 4-8 tasks.
- Use tool="search_web" when you need external info. Otherwise omit or set null.
- Keep tasks concise and executable.
"""


def _strip_code_fences(text: str) -> str:
    t = text.strip()
    if t.startswith("```"):
        # remove fenced blocks if model ignores instructions
        t = t.replace("```json", "").replace("```", "").strip()
    return t


class Planner:
    def __init__(self, llm: LLM):
        self.llm = llm

    def create(self, goal: str, previous_report: str | None, memory_snapshot: str) -> Plan:
        user = f"""Goal: {goal}

Previous report (if any):
{previous_report or "None"}

Recent memory/events:
{memory_snapshot}

Now create the plan JSON.
"""
        raw = self.llm.chat(
            [
                {"role": "system", "content": PLANNER_SYSTEM},
                {"role": "user", "content": user},
            ],
            temperature=0,
        )
        raw = _strip_code_fences(raw)

        data = json.loads(raw)
        return Plan.model_validate(data)
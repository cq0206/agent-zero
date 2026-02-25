import json
from typing import Any, Dict, List, Optional

from core.llm import LLM
from core.schema import Plan


PLANNER_SYSTEM = """You are an agent planner.

Return ONLY valid JSON following the schema:
{
  "tasks": [
    {
      "id": "t1",
      "description": "...",
      "expected_output": "...",
      "tool": "tool_name" | null,
      "args": { "param": "value" }
    }
  ]
}

Rules:
- Output ONLY JSON. No markdown, no code fences, no extra text.
- 4 to 8 tasks max.
- Use ONLY tools from the provided tool list. If none apply, set tool=null.
- If tool is not null, args MUST match that tool's params.
- Tasks must be concrete and executable. Avoid vague tasks like "do more research".
- expected_output must be verifiable (e.g., bullet list / table fields / decision with reasons).
"""


def _strip_code_fences(text: str) -> str:
    t = (text or "").strip()
    if t.startswith("```"):
        t = t.replace("```json", "").replace("```", "").strip()
    return t


def _safe_json_loads(text: str) -> Dict[str, Any]:
    """
    Robust JSON parse for occasional model slip-ups.
    Strategy:
    1) strip fences
    2) try json.loads
    3) if fails, try to extract the first {...} block
    """
    t = _strip_code_fences(text)

    try:
        return json.loads(t)
    except Exception:
        # Try best-effort extraction of the first JSON object
        start = t.find("{")
        end = t.rfind("}")
        if start != -1 and end != -1 and end > start:
            return json.loads(t[start : end + 1])
        raise


class Planner:
    """
    Planner creates a structured Plan from:
    - goal
    - prior report (for replan)
    - memory snapshot (persistent summary + recent events)
    - tool specs (white-listed tools)

    This version is designed to be:
    - machine-readable (schema)
    - executable (tool whitelist + args)
    - stable (hard constraints + low temperature)
    """

    def __init__(self, llm: LLM):
        self.llm = llm

    @staticmethod
    def _format_tool_specs(tool_specs: List[Dict[str, Any]]) -> str:
        """
        tool_specs element example:
        {
          "name": "search_web",
          "description": "Mock web search tool",
          "params": {"query": "string"}
        }
        """
        lines = []
        for spec in tool_specs:
            name = spec.get("name")
            desc = spec.get("description", "")
            params = spec.get("params", {})
            lines.append(f"- {name}: {desc} | params: {list(params.keys())}")
        return "\n".join(lines) if lines else "None"

    def create(
        self,
        goal: str,
        previous_report: Optional[str],
        memory_snapshot: str,
        tool_specs: List[Dict[str, Any]],
    ) -> Plan:

        tools_text = self._format_tool_specs(tool_specs)

        user_prompt = f"""Goal:
{goal}

Available tools (ONLY these are allowed):
{tools_text}

Memory snapshot (persistent summary + recent events):
{memory_snapshot}

Previous report (if any, for replanning):
{previous_report or "None"}

Now produce the plan JSON. Ensure every tool task has correct args.
"""

        raw = self.llm.chat(
            [
                {"role": "system", "content": PLANNER_SYSTEM},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0,
        )

        data = _safe_json_loads(raw)
        return Plan.model_validate(data)
import json
from typing import Any, Dict, List, Optional

from agent.recovery import RetryConfig, retry_json_parse
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
- Tasks must be concrete and executable.
- expected_output must be verifiable (bullets / fields / decisions).
"""


def _strip_code_fences(text: str) -> str:
    t = (text or "").strip()
    if t.startswith("```"):
        t = t.replace("```json", "").replace("```", "").strip()
    return t


def _safe_json_loads(text: str) -> Dict[str, Any]:
    t = _strip_code_fences(text)
    try:
        return json.loads(t)
    except Exception:
        start = t.find("{")
        end = t.rfind("}")
        if start != -1 and end != -1 and end > start:
            return json.loads(t[start:end + 1])
        raise


class Planner:
    def __init__(self, llm: LLM):
        self.llm = llm

    @staticmethod
    def _format_tool_specs(tool_specs: List[Dict[str, Any]]) -> str:
        lines = []
        for spec in tool_specs:
            name = spec.get("name")
            desc = spec.get("description", "")
            params = spec.get("params", {})
            lines.append(f"- {name}: {desc} | params: {list(params.keys())}")
        return "\n".join(lines) if lines else "None"

    @staticmethod
    def _format_recalled(recalled: List[Dict[str, Any]]) -> str:
        if not recalled:
            return "None"
        lines = []
        for r in recalled:
            lines.append(f"- (score={r['score']:.3f}) {r['text']} | meta={r.get('meta', {})}")
        return "\n".join(lines)

    def create(
        self,
        goal: str,
        previous_report: Optional[str],
        memory_snapshot: str,
        tool_specs: List[Dict[str, Any]],
        recalled_memories: List[Dict[str, Any]],
    ) -> Plan:

        tools_text = self._format_tool_specs(tool_specs)
        recalled_text = self._format_recalled(recalled_memories)

        user_prompt = f"""Goal:
{goal}

Available tools (ONLY these are allowed):
{tools_text}

Relevant long-term memories (may contain past learnings, constraints, preferences):
{recalled_text}

Memory snapshot (summary + recent events):
{memory_snapshot}

Previous report (if any, for replanning):
{previous_report or "None"}

Now produce the plan JSON. Ensure tool tasks have correct args.
"""

        raw = self.llm.chat(
            [
                {"role": "system", "content": PLANNER_SYSTEM},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0,
        )

        data = retry_json_parse(
            _safe_json_loads,
            raw,
            RetryConfig(max_retries=3),
        )
        return Plan.model_validate(data)

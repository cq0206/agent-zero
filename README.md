# Agent Zero

A minimal, production-oriented Agent runtime:

**Goal → Plan → Execute → Judge → Replan**

## Quick start

```bash
uv sync

# Option A: set environment variables directly
export OPENAI_API_KEY="..."
export OPENAI_MODEL="gpt-4o-mini"  # optional
export OPENAI_BASE_URL="https://api.openai.com/v1"  # optional
PYTHONPATH=. uv run python examples/company_research.py

# Option B: load from .env
set -a; source .env; set +a
PYTHONPATH=. uv run python examples/company_research.py
```

## Notes

- Run commands from the repository root.
- The first `uv run` may create `.venv` and install dependencies.
- `SearchWebTool` is currently a mock tool and returns placeholder search results.

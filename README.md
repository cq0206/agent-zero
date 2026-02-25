# 🚀 Agent Zero

**Minimal production-oriented Agent Runtime**  
Goal-driven autonomous system:  
**Plan → Execute → Judge → Replan → Memory**

[https://github.com/cq0206/agent-zero](https://github.com/cq0206/agent-zero)

---

## 💡 What is Agent Zero?

Agent Zero is a lightweight, extensible, and production-ready agent runtime framework designed to help you build autonomous, goal-driven AI systems.

### Key principles

✔ Structured planning (machine-readable)  
✔ Tool-driven execution  
✔ Reflection and re-planning  
✔ Persistent memory  
✔ Minimal but extensible architecture

---

## 🧠 Architecture Overview

```text
Data Sources / Tools → Planner → Plan (Tasks)
                         ↓
                      Executor
                         ↓
                        Judge
                         ↓
                    Memory Store
                         ↓
                    Replan / End
```

---

## 📦 Features (v0.x)

✅ Structured task planner  
✅ Executor with tool abstraction  
✅ Judge for plan validation  
✅ Persistent memory + auto summary  
✅ Clean OpenAI integration  
✅ Stable JSON schema plans

---

## 🚀 Quick Start

### 1) Clone

```bash
git clone https://github.com/cq0206/agent-zero.git
cd agent-zero
```

### 2) Setup env

Create `.env` with:

```env
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4o-mini
```

### 3) Install

```bash
pip install -e .
```

### 4) Run a demo

```bash
python examples/company_research.py
```

---
or
```bash
uv run agent-zero "Research Apple stock drivers"
```

## 🧪 Example Output

```text
# Report

## Goal
Research Tesla and produce a concise overview.

### t1: Basic Info
...
```

---

## 🛠 How it Works

### Planner

Generates a structured JSON plan via LLM.

### Executor

Executes tasks either via tools or native LLM.

### Judge

Checks plan results and signals re-planning.

### Memory

Keeps persistent events + summary for next runs.

---

## 🤝 Contributing

Contributions are welcome.

1. Fork the repo
2. Create your feature branch
3. Commit your changes
4. Push to your branch
5. Open a Pull Request

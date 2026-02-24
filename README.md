# 🧠 Agent Zero

> A minimal, goal-driven Agent runtime. Plan → Execute → Reflect → Evolve.↳

Agent Zero is a lightweight, production-oriented Agent runtime designed to explore the core architecture of autonomous systems — without hiding complexity behind heavy frameworks.↳

This project is built as a long-term technical asset and will evolve incrementally over the next 6–12 months.↳

## 🎯 Why Agent Zero?

Most “Agent frameworks” today fall into two categories:↳

* Workflow DSL engines↳
* Thin wrappers around LLM + tools↳

They often:↳

* Hide planning logic↳
* Mix orchestration with provider SDKs↳
* Lack clear runtime boundaries↳
* Cannot scale into production systems↳

Agent Zero focuses on one thing:↳

> Building a clean, interpretable Agent runtime core.

## 🧩 Core Philosophy

Agent Zero is built around a simple but strict loop:

`Goal`​` → Plan`​` → Execute`​` → Reflect`​` → Memory`​` → Replan`

Key principles:

* Goal-driven (not step-driven)
* Structured planning (machine-readable tasks)
* Explicit execution loop
* Evaluator-based reflection
* Pluggable memory
* Provider-agnostic LLM layer

No magic.

No hidden chains.

No black-box orchestration.

## 🏗 Architecture Overview

`agent-zero/ `​`│ `​`├── core/ `​`│   ├── llm.py        # Provider abstraction`​`│   ├── schema.py     # Structured task definitions`​`│ `​`├── agent/ `​`│   ├── planner.py `​`│   ├── executor.py `​`│   ├── judge.py `​`│   ├── runtime.py `​`│ `​`├── tools/ `​`│   ├── base.py `​`│   ├── search.py `​`│ `​`├── examples/ `​`│   ├── company_research.py`

### Runtime Flow

`User Goal `​`  ↓`​`Planner `​`  ↓`​`Structured Plan (JSON) `​`  ↓`​`Executor Loop`​`  ↓`​`Report `​`  ↓`​`Judge `​`  ↓`​`Replan (if needed)`

## 🚀 Current Capabilities (v0.1)

* Structured task planning
* Execution loop
* LLM-based evaluation↳
* Basic tool abstraction
* Provider abstraction layer↳

## 🔭 Roadmap

### Phase 1 — Minimal Closed Loop

* Planner
* Executor
* Judge
* Structured memory interface↳

### Phase 2 — Memory & Skills

* Vector memory↳
* Episodic memory↳
* Skill registry↳
* Tool permission model↳

### Phase 3 — Multi-Agent Runtime

* Role-based agents
* Agent-to-agent messaging↳
* Graph-based execution
* Async runtime↳

### Phase 4 — Production Hardening

* Observability
* Cost tracking
* Failure recovery
* State persistence↳
* Evaluation harness

## 🧠 Design Decisions

1. ### No Framework Lock-In

LLM providers are abstracted in `core/llm.py`.

You can swap:↳

* OpenAI
* Claude
* Local models
* Azure endpoints↳

Without touching the runtime.

2. ### Planning is Structured

Planning outputs must follow defined schemas.↳

This enables:

* Deterministic execution↳
* Debuggable task graphs↳
* Future static analysis

3. ### Reflection is Mandatory

An Agent without reflection is just a workflow.

Agent Zero treats evaluation as a first-class component.↳

## 🛠 Quick Start

`pip install -e .`

Set environment variables:↳

`OPENAI_API_KEY=your_key`

Run example:

`python examples/company_research.py`

## 📌 Intended Audience

* Engineers building production Agent systems
* Researchers exploring runtime architectures↳
* CTOs evaluating long-term AI infrastructure strategy↳

This is NOT:

* A beginner tutorial project↳
* A prompt collection
* A no-code agent builder

## 🧭 Long-Term Vision

Agent Zero aims to explore:

* What is the minimal runtime required for autonomous systems?
* How should planning be represented?
* How should memory evolve over time?↳
* Can we build interpretable, inspectable Agents?↳

This repository will evolve gradually, focusing on clarity over hype.↳

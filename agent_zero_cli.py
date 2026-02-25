import argparse

from core.llm import LLM
from agent.planner import Planner
from agent.executor import Executor
from agent.judge import Judge
from agent.runtime import AgentRuntime
from agent.memory import Memory
from tools.base import ToolRegistry
from tools.search import SearchWebTool


def main():
    parser = argparse.ArgumentParser("agent-zero")
    parser.add_argument("goal", type=str, help="Goal description for the agent")
    parser.add_argument("--rounds", type=int, default=3)
    args = parser.parse_args()

    llm = LLM()
    memory = Memory()
    tools = ToolRegistry()
    tools.register(SearchWebTool())

    planner = Planner(llm)
    executor = Executor(llm, tools, memory)
    judge = Judge(llm)
    runtime = AgentRuntime(planner, executor, judge, memory)

    report = runtime.run(args.goal, max_rounds=args.rounds)
    print("\n===== FINAL REPORT =====\n")
    print(report)


if __name__ == "__main__":
    main()

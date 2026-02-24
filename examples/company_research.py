from core.llm import LLM
from agent.planner import Planner
from agent.executor import Executor
from agent.judge import Judge
from agent.runtime import AgentRuntime
from agent.memory import Memory
from tools.base import ToolRegistry
from tools.search import SearchWebTool


def main():
    llm = LLM()  # OpenAI-only (OPENAI_API_KEY required)

    memory = Memory()
    tools = ToolRegistry()
    tools.register(SearchWebTool())

    planner = Planner(llm)
    executor = Executor(llm, tools, memory)
    judge = Judge(llm)

    runtime = AgentRuntime(planner, executor, judge, memory)

    company = "Tesla"
    goal = f"Research {company} and produce a concise business overview: products, moat, risks, and near-term outlook."
    report = runtime.run(goal, max_rounds=3)

    print(report)


if __name__ == "__main__":
    main()
from tools.base import Tool


class SearchWebTool(Tool):
    name = "search_web"
    description = "Mock web search tool. Returns placeholder info."

    def run(self, query: str) -> str:
        # v0.1: mock. v0.2+: replace with real search API / internal KB.
        return (
            f"[MOCK_SEARCH_RESULT]\n"
            f"Query: {query}\n"
            f"Notes: Replace this mock with real search integration later.\n"
        )
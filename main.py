import asyncio

from langchain_core.messages import HumanMessage
from langgraph.graph import END, START, StateGraph

from ag_workflows.planner_workflow import planner_node
from schemas.agent_schema import AgentState

graph = StateGraph(AgentState)
graph.add_node("planner", planner_node)

graph.add_edge(START, "planner")
graph.add_edge("planner", END)
app = graph.compile()


async def execute(query: str):
    """
    Async runner for the graph
    """

    initial_state: AgentState = {
        "query": [HumanMessage(content=query)],
    }  # type: ignore

    result = await app.ainvoke(initial_state)

    print(result["plan"])

    return result


if __name__ == "__main__":
    asyncio.run(
        execute(
            query="Get me the weather details for Singapore, New York, New Delhi and Tokyo. Apply leave for tomorrow(04-02-2026)"
        )
    )

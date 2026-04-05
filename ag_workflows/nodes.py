from langgraph.graph import END, START, StateGraph

from ag_workflows import executor_node, planner_node, summarizer_node
from schemas.agent_schema import AgentState


def should_continue(state: AgentState) -> str:
    plan = state.get("plan")

    if not plan or not plan.steps:
        return "summarizer"

    if all(step.status == "success" for step in plan.steps):
        return "summarizer"

    if all(step.status == "failed" for step in plan.steps):
        return "summarizer"

    return "executor"


graph = StateGraph(AgentState)
graph.add_node("planner", planner_node)
graph.add_node("executor", executor_node)
graph.add_node("summarizer", summarizer_node)

graph.add_edge(START, "planner")

graph.add_edge("planner", "executor")

# Run the executor until all steps either success or failed
graph.add_conditional_edges(
    "executor",
    should_continue,
    {
        "executor": "executor",
        "summarizer": "summarizer",
    },
)

graph.add_edge("summarizer", END)

app = graph.compile()

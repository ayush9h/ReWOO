from langgraph.graph import END, START, StateGraph

from ag_workflows import planner_node, executor_node, summarizer_node
from schemas.agent_schema import AgentState


def should_continue(state: AgentState) -> str:
    plan = state.get("plan")

    if not plan or not plan.steps:
        return "summarizer_node"

    if all(step.status == "success" for step in plan.steps):
        return "summarizer_node"

    if all(step.status == "failed" for step in plan.steps):
        return "summarizer_node"

    return "executor_node"


graph = StateGraph(AgentState)
graph.add_node("planner", planner_node)
graph.add_node("executor", executor_node)
graph.add_node("summarizer", summarizer_node)

graph.add_edge(START, "planner")

# Run the executor until all steps either success or failed
graph.add_edge("planner", "executor")

graph.add_conditional_edges(
    "executor",
    should_continue,
    {
        "executor_node": "executor",
        "summarizer_node": "summarizer",
    },
)

graph.add_edge("summarizer_node", END)

app = graph.compile()

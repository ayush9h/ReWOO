from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph

from ag_workflows import (executor_node, hitl_node, planner_node,
                          summarizer_node)
from schemas.agent_schema import AgentState


def should_continue(state: AgentState) -> str:
    plan = state.get("plan")

    if not plan or not plan.steps:
        return "summarizer"

    if any(step.status == "pending_human_approval" for step in plan.steps):
        return "hitl"

    if all(step.status in {"success", "failed"} for step in plan.steps):
        return "summarizer"

    steps_mp = {s.step_id: s for s in plan.steps}

    has_ready_step = False

    for step in plan.steps:
        if step.status != "pending":
            continue

        # Fail the steps due to dependency never completed
        if any(steps_mp[d].status == "failed" for d in step.depends_on):
            step.status = "failed"
            step.evidence.content = "Failed because dependency failed"
            continue

        # If all dependencies succeeded, executor can run it.
        if all(steps_mp[d].status == "success" for d in step.depends_on):
            has_ready_step = True

    if has_ready_step:
        return "executor"

    return "summarizer"


checkpointer = InMemorySaver()
graph = StateGraph(AgentState)
graph.add_node("planner", planner_node)
graph.add_node("executor", executor_node)
graph.add_node("summarizer", summarizer_node)
graph.add_node("hitl", hitl_node)


graph.add_edge(START, "planner")

graph.add_edge("planner", "executor")


graph.add_conditional_edges(
    "executor",
    should_continue,
    {
        "executor": "executor",
        "summarizer": "summarizer",
        "hitl": "hitl",
    },
)
graph.add_edge("hitl", "executor")
graph.add_edge("summarizer", END)

app = graph.compile(checkpointer=checkpointer)

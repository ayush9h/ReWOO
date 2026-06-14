from langgraph.types import interrupt

from schemas.agent_schema import AgentState


def hitl_node(state: AgentState):
    """
    Checks for the step with `pending_human_approval` and raises an interrupt
    """

    plan = state.get("plan")
    if not plan:
        return state

    step = next(s for s in plan.steps if s.status == "pending_human_approval")

    user_approval = interrupt(
        {
            "message": "Approve tool execution",
            "tool_name": step.evidence.tool_name,
            "tool_input": step.evidence.tool_input,
        }
    )
    if user_approval.get("approved"):
        step.evidence.tool_input["_human_approved"] = True
        step.evidence.content = "human approved"
        step.status = "pending"
    else:
        step.evidence.content = "human rejected the request"
        step.status = "failed"

    return state

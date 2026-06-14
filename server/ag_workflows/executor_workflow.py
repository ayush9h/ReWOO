from typing import Dict

from ag_workflows.tools import TOOL_REGISTRY
from schemas.agent_schema import AgentState


def is_step_ready(step, steps_mp: Dict):
    if step.status != "pending":
        return False

    for dep_id in step.depends_on:
        dep = steps_mp.get(dep_id)
        if not dep or dep.status != "success":
            return False

    return True


def get_ready_steps(plan):
    steps_mp = {s.step_id: s for s in plan.steps}

    return [step for step in plan.steps if is_step_ready(step, steps_mp)]


async def execute(step):
    """
    Executes a step by tool calling and human approval checks
    """
    try:
        tool = TOOL_REGISTRY.get(step.evidence.tool_name)
        if not tool:
            raise ValueError("Tool Not found in the registry, please check again")

        require_approval = tool.get("require_approval")
        approved = step.evidence.tool_input.get("_human_approved", False)

        # If tool requires approval and user not approved
        if require_approval and not approved:
            step.status = "pending_human_approval"
            step.evidence.content = f"Human approval required for tool:{tool}"

            return

        # Run the tool as dependency resolved
        step.status = "running"
        result = await tool["fn"](step.evidence.tool_input)

        step.evidence.content = result
        step.status = "success"

    except Exception as e:
        step.evidence.content = f"Failure due to {e}"
        step.status = "failed"


async def executor_node(state: AgentState) -> AgentState:
    plan = state.get("plan")

    if not plan or not plan.steps:
        return state

    curr_ready_steps = get_ready_steps(plan)

    # Run the steps sequentially(can be improved) for parallel execution for non-dependent calls.
    for step in curr_ready_steps:
        await execute(step)

    return state

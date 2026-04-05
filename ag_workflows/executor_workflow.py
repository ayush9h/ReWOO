from schemas.agent_schema import AgentState


def executor_node(state: AgentState):
    print(f"Inside the eexeuctor node: {state}")

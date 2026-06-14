from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq

from config.development import settings
from schemas.agent_schema import AgentState

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=settings.GROQ_API_KEY,
    streaming=False,
)


def build_execution_context(plan) -> str:
    lines = []

    for step in sorted(plan.steps, key=lambda x: x.step_id):
        lines.append(f"Step {step.step_id}: {step.plan}")
        lines.append(f"Status: {step.status}")
        lines.append(f"Output: {step.evidence.content}")
        lines.append("")

    return "\n".join(lines)


async def summarizer_node(state: AgentState) -> AgentState:
    plan = state.get("plan")

    if not plan or not plan.steps:
        state["final_response"] = "No result generated."
        return state

    execution_context = build_execution_context(plan)

    messages = [
        SystemMessage(
            content="""
You are a helpful assistant.

Convert the execution results into a clean, user-friendly response.

Rules:
- Do not mention steps
- Do not mention tools
- Combine all useful information
- If something failed, mention it briefly
- Be concise and natural
"""
        ),
        HumanMessage(content=execution_context),
    ]

    response = await llm.ainvoke(messages)

    state["final_response"] = str(response.content)

    return state

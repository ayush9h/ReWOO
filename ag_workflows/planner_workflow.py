"""
Implementation of the planner agnet node
"""
from langchain_core.messages import SystemMessage
from langchain_groq import ChatGroq

from config.development import settings
from prompts.planner import planner_prompt_parser
from schemas.agent_schema import AgentState

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    streaming=True,
    api_key=settings.GROQ_API_KEY,
)


async def planner_node(state: AgentState) -> AgentState:
    planner_prompt, planner_parser = planner_prompt_parser()

    planner_prompt = planner_prompt.format(
        query=state.get("query")[-1],
    )

    messages = [
        SystemMessage(content=planner_prompt),
        *state.get("query", ""),
    ]

    output = await llm.ainvoke(messages)
    generated_plan = planner_parser.parse(output.content)  # type:ignore

    state["plan"] = generated_plan
    return state

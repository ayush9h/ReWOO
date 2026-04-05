import asyncio

from langchain_core.messages import HumanMessage

from ag_workflows.nodes import app
from schemas.agent_schema import AgentState


async def execute(query: str):

    initial_state: AgentState = {
        "query": [HumanMessage(content=query)],
    }  # type: ignore

    result = await app.ainvoke(initial_state)

    return result.get("final_response", "")


if __name__ == "__main__":
    # Test Application
    asyncio.run(
        execute(
            query="Policy for company car and leave. Apply leave for tomorrow(04-02-2026)"
        )
    )

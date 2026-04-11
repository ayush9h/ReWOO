from ag_workflows.nodes import app
from fastapi import APIRouter
from langchain_core.messages import HumanMessage
from schemas import AgentState, QueryParams

chat_router = APIRouter(prefix="/chat", tags=["User chats with the agent"])


@chat_router.post("/conversation")
async def conversation(state: QueryParams):

    initial_state: AgentState = {
        "query": [
            HumanMessage(content=state.query),
        ],
    }  # type: ignore
    result = await app.ainvoke(initial_state)
    return result

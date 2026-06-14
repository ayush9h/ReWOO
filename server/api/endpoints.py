import uuid

from fastapi import (APIRouter, WebSocket, WebSocketDisconnect,
                     WebSocketException)
from langchain_core.messages import HumanMessage
from langchain_core.runnables.config import RunnableConfig
from langgraph.types import Command
from starlette.websockets import WebSocketState

from ag_workflows.nodes import app
from schemas import AgentState

chat_router = APIRouter(
    prefix="/conversation",
    tags=[
        "User chats with the agent",
        "Request id generation for websocket connection",
    ],
)


@chat_router.post("/c")
async def generate_req():
    """
    Generates a request_id for the current conversations

    Params:
     - None

    Return
     - request_id: str = Unique request id for the current user
    """
    request_id: str = str(uuid.uuid4())

    return {"request_id": request_id}


@chat_router.websocket("/c/{request_id}")
async def conversation(websocket: WebSocket, request_id: str):
    await websocket.accept()

    thread_id = request_id or str(uuid.uuid4())

    config: RunnableConfig = RunnableConfig(
        configurable={"thread_id": thread_id},
    )

    async def stream_graph(graph_input):
        async for chunk in app.astream(graph_input, config=config):
            if "__interrupt__" in chunk:
                interrupt_obj = chunk["__interrupt__"][0]

                await websocket.send_json(
                    {
                        "type": "interrupt",
                        "data": interrupt_obj.value,
                    }
                )
                return "interrupted"

            if "planner" in chunk:
                planner_data = chunk.get("planner")

                if planner_data:
                    plan = planner_data.get("plan")

                    if plan:
                        await websocket.send_json(
                            {
                                "type": "plan",
                                "data": [step.plan for step in plan.steps],
                            }
                        )

            if "summarizer" in chunk:
                summarizer_data = chunk.get("summarizer") or {}
                final_resp = summarizer_data.get("final_response")

                await websocket.send_json(
                    {
                        "type": "summarizer",
                        "data": str(final_resp),
                    }
                )

        await websocket.send_json({"type": "done"})
        return "done"

    try:
        while True:
            data = await websocket.receive_json()
            msg_type = data.get("type", "query")

            if msg_type == "query":
                query = data.get("query", "").strip()

                if not query:
                    await websocket.send_json(
                        {
                            "type": "error",
                            "data": "Query cannot be empty",
                        }
                    )
                    continue

                initial_state: AgentState = {
                    "query": [
                        HumanMessage(content=query),
                    ],
                }  # type: ignore

                await stream_graph(initial_state)

            elif msg_type == "resume":
                approved = bool(data.get("approved"))

                await stream_graph(Command(resume={"approved": approved}))

            else:
                await websocket.send_json(
                    {
                        "type": "error",
                        "data": f"Unknown message type: {msg_type}",
                    }
                )

    except WebSocketDisconnect:
        return

    except WebSocketException as e:
        try:
            await websocket.send_json(
                {
                    "type": "error",
                    "data": f"Error occurred in the system due to: {e}",
                }
            )
        except Exception:
            pass

    except Exception as e:
        try:
            await websocket.send_json(
                {
                    "type": "error",
                    "data": f"Unexpected error occurred due to: {e}",
                }
            )
        except Exception:
            pass

    finally:
        if websocket.client_state == WebSocketState.CONNECTED:
            await websocket.close(code=1000)

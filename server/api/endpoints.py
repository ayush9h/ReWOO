import uuid

from ag_workflows.nodes import app
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, WebSocketException
from langchain_core.messages import HumanMessage
from schemas import AgentState
from starlette.websockets import WebSocketState

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
async def conversation(websocket: WebSocket):
    """
    Establishes a connection with the received request_id
    """
    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_json()
            query = data.get("query")
            initial_state: AgentState = {
                "query": [
                    HumanMessage(content=query),
                ],
            }  # type: ignore
            async for chunk in app.astream(initial_state):

                # Send the planner data to the UI
                if "planner" in chunk:
                    planner_data = chunk.get("planner")

                    if planner_data:
                        plan = planner_data.get("plan", "")
                        await websocket.send_json(
                            {
                                "type": "plan",
                                "data": [step.plan for step in plan.steps],
                            }
                        )

                # Send the final response to THe UI
                if "summarizer" in chunk:
                    final_resp = chunk.get("summarizer", "").get("final_response")
                    await websocket.send_json(
                        {
                            "type": "summarizer",
                            "data": f"{final_resp}",
                        }
                    )

            await websocket.send_json({"type": "done"})

    except WebSocketDisconnect:
        return
    except WebSocketException as e:
        if websocket:
            try:
                await websocket.send_json(
                    {
                        "type": "error",
                        "data": f"Error occurred in the system due to: {e}",
                    }
                )
            except:
                pass

    finally:
        if websocket.client_state == WebSocketState.CONNECTED:
            await websocket.close(
                code=1000, reason="Streaming completed without failure"
            )

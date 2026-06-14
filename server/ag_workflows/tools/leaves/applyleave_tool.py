from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage

from config.llm import summarizer_llm


async def applyleave_tool(input_data: dict[str, Any]) -> str:
    """
    Requires human approval before applying the leave to the portal.

    Note:
    Human approval should be enforced from TOOL_REGISTRY / HITL flow,
    not inside this tool directly.
    """

    messages = [
        SystemMessage(
            content=(
                "You are an HR leave management assistant. "
                "Generate a clear, professional confirmation response for a leave application. "
                "Do not claim the leave was actually applied in a real portal unless the input confirms it. "
                "Keep the response generic and user-friendly."
            )
        ),
        HumanMessage(
            content=(
                "Generate a leave application confirmation response for this input:\n\n"
                f"{input_data}"
            )
        ),
    ]

    response = await summarizer_llm.ainvoke(messages)

    return str(response.content).strip()

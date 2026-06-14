from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage

from config.llm import summarizer_llm


async def outofoffice_tool(input_data: dict[str, Any]) -> str:
    """
    Generates a generic out-of-office confirmation response.
    """

    messages = [
        SystemMessage(
            content=(
                "You are an HR/workplace assistant. "
                "Generate a clear, professional confirmation response for setting an out-of-office status. "
                "Do not claim the status was actually updated in a real system unless the input confirms it. "
                "Keep the response generic and concise."
            )
        ),
        HumanMessage(
            content=(
                "Generate an out-of-office confirmation response for this input:\n\n"
                f"{input_data}"
            )
        ),
    ]

    response = await summarizer_llm.ainvoke(messages)

    return str(response.content).strip()

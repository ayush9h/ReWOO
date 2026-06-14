from langchain_core.messages import HumanMessage, SystemMessage

from config.llm import summarizer_llm


async def summarize_tool(input_data: str) -> str:
    if not input_data or not input_data.strip():
        return "No content was provided to summarize."

    messages = [
        SystemMessage(
            content=(
                "You are a document summarization assistant. "
                "Create a concise summary of the given content. "
                "Use a professional tone. "
                "Include key points, important details, and action items if present. "
                "Do not invent missing information."
            )
        ),
        HumanMessage(
            content=(
                "Document/content:\n\n"
                f"{input_data}\n\n"
                "Return the summary in this format:\n"
                "Summary:\n"
                "- Key point 1\n"
                "- Key point 2\n\n"
                "Action Items:\n"
                "- Action item if present, otherwise say None"
            )
        ),
    ]

    response = await summarizer_llm.ainvoke(messages)

    return str(response.content).strip()

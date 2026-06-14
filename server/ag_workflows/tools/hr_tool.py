from langchain_core.messages import HumanMessage, SystemMessage

from config.llm import summarizer_llm


async def hr_tool(input_data: dict) -> str:
    messages = [
        SystemMessage(
            content=(
                "You are an HR assistant. Generate a clear, generic, professional "
                "HR policy-style response based on the given input. Do not claim to "
                "know the company's actual policy unless it is explicitly provided."
            )
        ),
        HumanMessage(
            content=f"Generate a generic HR response for this input:\n\n{input_data}"
        ),
    ]

    response = await summarizer_llm.ainvoke(messages)

    return str(response.content).strip()

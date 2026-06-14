from langchain_groq import ChatGroq

from config.development import settings

summarizer_llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=settings.GROQ_API_KEY,
    streaming=False,
)


planner_llm = ChatGroq(
    model="openai/gpt-oss-20b",
    streaming=True,
    reasoning_effort=None,
    reasoning_format=None,
    api_key=settings.GROQ_API_KEY,
)

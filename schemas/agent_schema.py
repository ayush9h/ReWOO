from typing import Annotated, List, TypedDict

from langchain_core.messages import HumanMessage
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    query: Annotated[List[HumanMessage], add_messages]

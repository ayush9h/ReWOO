from typing import Annotated, List, Optional, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

from schemas.plan_schema import Plan


class AgentState(TypedDict):
    query: Annotated[List[BaseMessage], add_messages]
    plan: Optional[Plan] | None

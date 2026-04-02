from typing import Any, List, Literal, Optional

from pydantic import BaseModel, Field


class Evidence(BaseModel):
    id: str = Field(
        description="Identifier of the evidence in the form of #E1, #E2 etc.",
    )
    content: Optional[str] = Field(
        default=None,
        description="Output from the worker after running the tool if present",
    )
    tool_name: Literal["WeatherTool", "LeaveTool"] | None
    tool_input: dict[str, Any] = Field(
        description="Inputs valid for the tool execution"
    )


class Step(BaseModel):
    step_id: int = Field(
        description="Step number",
    )
    plan: str = Field(
        description="Instruction for the worker to execute itself",
    )
    evidence: Evidence = Field(description="Placeholder for the result")


class Plan(BaseModel):
    steps: List[Step] = Field(
        description="Ordered list of execution steps for the completion of the task",
    )

from .hr_tool import hr_tool
from .leaves import applyleave_tool, outofoffice_tool
from .summarize_tool import summarize_tool

TOOL_REGISTRY = {
    "HRTool": {
        "name": "HRTool",
        "description": "Handles HR operations for policy questions asked by the user.",
        "input_schema": {
            "type": "object",
            "properties": {"query": {"type": "string"}},
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "message": {"type": "string"},
            },
        },
        "fn": hr_tool,
        "depends_on": None,
        "next_tool": None,
    },
    "SummaryTool": {
        "name": "SummaryTool",
        "description": "Generates concise summaries from input text.",
        "input_schema": {
            "type": "object",
            "properties": {
                "text": {"type": "string"},
            },
        },
        "output_schema": {
            "type": "object",
            "properties": {"summary": {"type": "string"}},
        },
        "fn": summarize_tool,
        "depends_on": None,
        "next_tool": None,
    },
    "LeaveTool": {
        "name": "LeaveTool",
        "description": "Executes when the user wants to apply for leave",
        "input_schema": {
            "type": "object",
            "properties": {
                "text": {"type": "string"},
            },
        },
        "output_schema": {
            "type": "object",
            "properties": {"summary": {"type": "string"}},
        },
        "fn": applyleave_tool,
        "depends_on": None,
        "next_tool": "OutOfOfficeTool",
    },
    "OutOfOfficeTool": {
        "name": "OutOfOfficeTool",
        "description": "Generally executes when the user successfully applies for leave, or directly asks for outofoffice",
        "input_schema": {
            "type": "object",
            "properties": {
                "text": {"type": "string"},
            },
        },
        "output_schema": {
            "type": "object",
            "properties": {"summary": {"type": "string"}},
        },
        "fn": outofoffice_tool,
        "depends_on": ["LeaveTool"]
        or None,  # It depends on the execution of LeaveTool,
        "next_tool": None,
    },
}

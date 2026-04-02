from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate

from schemas.plan_schema import Plan


def planner_prompt_parser():
    """
    Planner Prompt setup
    """
    parser = PydanticOutputParser(pydantic_object=Plan)

    prompt = PromptTemplate(
        template="""
    You are a **STRICT** planning agent in a ReWOO system.

    Your job is **ONLY** to generate a structured execution plan.

    User Query:
    {query}

    **IMP**
     - Evidence content is empty at this stage. Do not add anything in that.
     - Collate inputs wherever possible, keep steps as minimum as possible.
    Return **ONLY** valid JSON matching schema.

    {format_instructions}
    """,
        input_variables=["query"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    return prompt, parser

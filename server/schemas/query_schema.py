from pydantic import BaseModel, Field


class QueryParams(BaseModel):
    query: str = Field(description="User original query")

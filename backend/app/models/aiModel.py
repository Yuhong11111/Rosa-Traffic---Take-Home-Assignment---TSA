from typing import List, Optional, Any
from pydantic import BaseModel, Field


class AssistantRequest(BaseModel):
    question: str


class FilterCondition(BaseModel):
    field: str
    operator: str
    value: str


class FilterObject(BaseModel):
    conditions: List[FilterCondition] = Field(default_factory=list)
    operation: Optional[str] = None
    sort_by: Optional[str] = None
    sort_direction: Optional[str] = None


class AssistantResponse(BaseModel):
    # filter: FilterObject
    result: Any = None

from pydantic import BaseModel


class AssistantRequest(BaseModel):
    question: str

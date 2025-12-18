import json
from fastapi import APIRouter, HTTPException
from ..model.models import AssistantRequest

router = APIRouter()

@router.post("/api/assistant")
async def assistant_endpoint(payload: AssistantRequest):
    question = payload.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    return {"message": "Assistant response", "data": question}

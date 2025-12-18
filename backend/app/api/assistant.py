import re
from fastapi import APIRouter, HTTPException
from ..models.aiModel import (
    AssistantRequest,
    AssistantResponse,
    FilterCondition,
    FilterObject,
)

router = APIRouter()


def build_mock_filter(question: str) -> FilterObject:
    """Mock the behavior of an LLM by deriving a structured filter from heuristics."""
    question_lower = question.lower()
    conditions = []

    # Direction filters
    if "north" in question_lower:
        conditions.append(
            FilterCondition(field="Direction", operator="==", value="North")
        )
    elif "south" in question_lower:
        conditions.append(
            FilterCondition(field="Direction", operator="==", value="South")
        )

    # Speed filters
    speed_match = re.search(r"(\d+)\s*(?:kph|km/h|mph)?", question_lower)
    if speed_match:
        speed_value = speed_match.group(1)
        if any(keyword in question_lower for keyword in ["faster", "over", "greater", "above"]):
            conditions.append(
                FilterCondition(field="Speed", operator=">", value=speed_value)
            )
        elif any(keyword in question_lower for keyword in ["slower", "under", "below", "less"]):
            conditions.append(
                FilterCondition(field="Speed", operator="<", value=speed_value)
            )

    # Lane filters
    lane_match = re.search(r"lane\s*(\d+)", question_lower)
    if lane_match:
        lane_value = lane_match.group(1)
        conditions.append(
            FilterCondition(field="Lane", operator="==", value=lane_value)
        ) 

    # Time filters
    # (This is a simplified example; real implementation would need robust date parsing)
    time_match = re.search(r"after\s*([\d-]+)", question_lower)
    if time_match:
        time_value = time_match.group(1)
        conditions.append(
            FilterCondition(field="Timestamp", operator=">", value=time_value)
        )

    # Determine operation
    operation = "filter"
    if "how many" in question_lower or "count" in question_lower:
        operation = "count_vehicles"
    elif "average" in question_lower:
        operation = "average_speed"
    elif "max" in question_lower or "highest" in question_lower:
        operation = "max_speed"
    elif "list" in question_lower or "show me" in question_lower:
        operation = "list_vehicles"

    # Sorting instructions
    sort_by = None
    if "sorted by speed" in question_lower or "order by speed" in question_lower:
        sort_by = "speed_kph"

    return FilterObject(
        conditions=conditions,
        operation=operation,
        sort_by=sort_by,
    )


@router.post("/api/assistant", response_model=AssistantResponse)
async def assistant_endpoint(payload: AssistantRequest):
    question = payload.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    filter_object = build_mock_filter(question)
    message = (
        "Structured JSON filter generated from query."
        if filter_object.conditions
        else "Structured JSON filter created without specific conditions."
    )

    return AssistantResponse(
        message=message,
        filter=filter_object,
    )

import json
import re
from fastapi import APIRouter, HTTPException
from pydantic import ValidationError
from ..models.aiModel import (
    AssistantRequest,
    AssistantResponse,
    FilterCondition,
    FilterObject,
)
# Commented out the python filter engine
# from ..services.filter_engine import process_filter
from ..services.sql_engine import generate_sql_query, execute_sql_query

router = APIRouter()

VALID_OPERATORS = {"==", "!=", ">", "<", ">=", "<="}


def build_mock_filter(question: str) -> FilterObject:
    # For production: replace this heuristic with a real LLM call that emits the
    # structured filter JSON described in docs/llm_integration.md, then validate
    # with validate_json before processing.
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

    # Determine operation
    operation = ""
    if "how many" in question_lower or "count" in question_lower:
        operation = "count_vehicles"
    elif "average" in question_lower:
        operation = "average_speed"
    elif "max" in question_lower or "highest" in question_lower:
        operation = "max_speed"
    elif "list" in question_lower or "show me" in question_lower:
        operation = "list_vehicles"

    # Check if there are conditions or operation early
    if not conditions and not operation:
        raise ValueError("Question must include at least one filter condition or an operation (count, average, max, list).")

    # Sorting instructions
    sort_by = None
    sort_direction = None
    if "sorted by speed" in question_lower or "order by speed" in question_lower:
        sort_by = "Speed"
    elif "sorted by lane" in question_lower or "order by lane" in question_lower:
        sort_by = "Lane"
    elif "sorted by time" in question_lower or "order by time" in question_lower or "sorted by collection" in question_lower:
        sort_by = "CollectionTime"
    
    if "ascending" in question_lower or "from lowest to highest" in question_lower:
        sort_direction = "ascending"
    elif "descending" in question_lower or "from highest to lowest" in question_lower:
        sort_direction = "descending"
    else:
        # Default to ascending if sorting is mentioned but no direction specified
        if sort_by:
            sort_direction = "ascending"

    return FilterObject(
        conditions=conditions,
        operation=operation,
        sort_by=sort_by,
        sort_direction=sort_direction,
    )


# mimic LLM response generation(JSON format)
def generate_mock_llm_response(question: str) -> str:
    # get pydantic model and convert to python dict using model_dump
    filter_payload = build_mock_filter(question).model_dump()
    # convert to json string
    return json.dumps(filter_payload)


def validate_json(raw_response: str) -> FilterObject:
    try:
        data = json.loads(raw_response)
    except json.JSONDecodeError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"LLM returned malformed JSON: {exc.msg}",
        ) from exc

    if not isinstance(data, dict):
        raise HTTPException(status_code=502, detail="LLM response must be a JSON object.")

    conditions = data.get("conditions", [])
    if not isinstance(conditions, list):
        raise HTTPException(status_code=502, detail="'conditions' must be a list.")

    for index, condition in enumerate(conditions):
        # ensure condition has required keys
        if not all(key in condition for key in ("field", "operator", "value")):
            raise HTTPException(
                status_code=502,
                detail=f"Condition #{index + 1} missing required keys (field/operator/value).",
            )
        operator = condition["operator"]
        # ensure operator is valid
        if operator not in VALID_OPERATORS:
            raise HTTPException(
                status_code=502,
                detail=f"Condition #{index + 1} contains invalid operator '{operator}'.",
            )

    try:
        return FilterObject(**data)
    except ValidationError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Filter validation failed: {exc.errors()}",
        ) from exc


@router.post("/api/assistant", response_model=AssistantResponse)
async def assistant_endpoint(payload: AssistantRequest):
    question = payload.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    # Mock LLM response generation
    try:
        raw_response = generate_mock_llm_response(question)
    except ValueError as exc:
        # Catch early validation from build_mock_filter
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    
    # Validate and parse the response
    filter_object = validate_json(raw_response)
    
    # Generate SQL query
    sql_query = generate_sql_query(filter_object)
    
    # Execute SQL and get the result
    result = execute_sql_query(sql_query)
    
    # Comment out Python filter engine result
    # result = process_filter(filter_object)

    return AssistantResponse(
        # filter=filter_object,
        result=result,
        sql=sql_query,
    )

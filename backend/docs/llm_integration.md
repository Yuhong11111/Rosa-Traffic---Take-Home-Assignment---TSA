# LLM Integration Notes

## Goal
Use a real LLM (OpenAI/Claude/etc.) to convert a natural-language query into a structured filter JSON that our backend can validate and execute.

## Expected JSON shape
```json
{
  "conditions": [
    { "field": "Direction", "operator": "==", "value": "North" },
    { "field": "Speed", "operator": ">", "value": "55" }
  ],
  "operation": "list|count|average|max|min",
  "sort_by": "Speed",
  "sort_direction": "ascending|descending"
}
```
- `conditions` is a list of dicts; each must have `field`, `operator`, `value`.
- Allowed operators: `==`, `!=`, `>`, `<`, `>=`, `<=`.
- If no operation is specified, default to `list`.
- If sorting is requested without direction, default to `ascending`.

## Prompt sketch
```
You are a filter-extraction assistant. Given a short, single-sentence natural-language query about traffic data, return ONLY a JSON object with the keys "operation", "conditions", and optionally "sort_by" and "sort_direction". Return no explanation or extra text.

Rules:

1. conditions
- Always return "conditions" as a list. Use an empty list if the query has no filters.
- Each condition must contain: "field", "operator", "value".
- All "value" fields must be returned as strings, even if they look numeric (e.g., "55").
- Do not infer or invent filters that the user did not explicitly mention.

2. operation
- Supported operations (as strings): "list", "count", "average", "max", "min".
- If the user does not specify an operation, set "operation" to "list".

3. operators
Allowed operators: "==", "!=", ">", "<", ">=", "<=", "contains"

4. fields
Allowed fields: "Direction", "Speed", "Lane", "CollectionTime"

5. sorting
- If the query requests sorting, include "sort_by" and "sort_direction".
- "sort_direction" must be "ascending" or "descending".
- If sorting direction is not specified by the user, default to "ascending".

6. value formatting
- ALL values must be strings (e.g., "North", "55", "2025-12-07 10:00:00").

Example output:
{
  "conditions": [
    { "field": "Direction", "operator": "==", "value": "North" },
    { "field": "Speed", "operator": ">", "value": "55" }
  ],
  "operation": "count",
  "sort_by": "Speed",
  "sort_direction": "descending"
}
```

## Call pattern (example)
1) Build the prompt with the user question appended.
2) Call LLM completion API.
3) Parse the string as JSON.
4) Run `validate_json` (in `assistant.py`) to enforce structure/operators.
5) Process the resulting `FilterObject` with `process_filter` / SQL engine.

### Suggested model params
- Use a low temperature (e.g., 0–0.2) to minimize creativity and stick to the user’s intent.
- Keep max tokens small; the response is a short JSON.
- Disable or avoid additional system prompts that might add prose; we only want structured JSON.

## Future extensions
- Expand fields/conditions beyond the current sample (e.g. time ranges, expression like "after 10 AM") and update the operator allowlist accordingly.
- Add more operations (e.g., min speed, group by) and reflect them in the prompt and validation.

## Error handling
- If JSON parsing fails or required keys/operators are missing, return 502 with a clear message.
- If the LLM omits `conditions`, you can either treat it as empty (and default operation to `list`) or reject with 400 to avoid unconstrained “SELECT *” queries.
- Reject conditions that have empty `field`/`operator`/`value` to prevent malformed filters.

## Security / safety
- Do not execute raw LLM output; always validate and coerce via `FilterObject`.

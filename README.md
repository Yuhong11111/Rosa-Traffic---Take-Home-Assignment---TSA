# Rosa-Traffic---Take-Home-Assignment---TSA

This is a take home project from TSA. The main focus will be on an AI query assistant.

## Getting Started

### Requirements

- Node.js 18+ and npm
- Python 3.10+ (with `venv`)

### Frontend (React + Vite)

```bash
cd frontend
npm install        # only needed the first time
npm run dev
```

The dev server prints a local URL (default `http://localhost:5173`). Open it in your browser.

### Backend (FastAPI)

```bash
cd backend
source .venv/bin/activate  # or .venv\\Scripts\\activate on Windows
uvicorn app.main:app --reload --port 8000
```

### Running Tests

From the repo root (with your virtualenv active):

```bash
python -m unittest discover backend/tests -t backend
```

This runs the assistant, filter engine, and SQL engine unit tests.

## Design Choices

**Modular project structure**  
The project is organized into separate modules for pages, services, data loading, and Pydantic models. This modularity keeps the code maintainable, reusable, and easier to extend.

**Clear and safe API communication**  
The frontend communicates with the FastAPI backend using Axios with explicit CORS settings. This ensures secure and predictable communication between frontend and backend.

**Structured JSON Query Schema**  
A consistent schema (`FilterObject` and `FilterCondition`) is used to represent extracted queries. Pydantic enforces type safety and ensures malformed or incomplete JSON is caught before execution.

**Simple, focused frontend**  
The UI is intentionally minimal. Its purpose is to clearly demonstrate the query and result.

**Mocked LLM with helper function**  
Instead of calling a real LLM, I implemented a mocked LLM step that extracts keywords and generates a structured `FilterObject`. It detects:
- direction comparisons (“north”, “south”)
- speed comparisons
- lane comparisons
- sorting requests
- the appropriate operation (“list”, “count”, “average”, “max”, “min”)

Although mocked, the system is designed so a real LLM can be integrated later with minimal changes.

**Thorough validation**  
Two layers of validation are used:
1. **Model-level validation** via Pydantic  
2. **Functional checks** for valid fields, operators, and operations  

This prevents invalid JSON from reaching the filter/aggregation logic.

---

## Tradeoffs

**Single-turn queries only**  
The system handles each query independently. This makes the pipeline simple and fast but prevents follow-up questions that rely on conversational context.

**Mocked LLM instead of real LLM**  
The mocked LLM captures only the patterns explicitly programmed. A real LLM would handle more natural phrasing, but mocking ensures deterministic behavior and eliminates the need for LLM API keys.

**In-memory dataset**  
The dataset is loaded from a CSV file into memory. This is sufficient for this assignment scope but not optimal for large-scale or concurrent workloads.

---

## Mocked LLM Behavior

The mocked LLM simulates the behavior of a real model:

1. It inspects the user query for:
   - `Direction` (North/South)
   - `Speed` conditions
   - `Lane` references
   - Sorting requests
   - Operation classification

2. It constructs a valid `FilterObject`  
3. Converts it into JSON, mimicking a real LLM style  
4. Passes it through validation  
5. The backend executes the filter and returns formatted results

This fully exercises the LLM → JSON → validation → execution pipeline.

---

## How I Used AI Tools

I used ChatGPT as a reasoning and reference assistant to:

- Set up and validate the development environment  
- Clarify assignment requirements and correct workflow   
- Assist with frontend sizing/layout issues  
- Draft longer conditional patterns for mock LLM logic
- Suggest error-handling and validation strategies
- Suggest an initial testing setup
- Improve documentation clarity  

---

## Future Improvements

**Automated testing**  
Add unit tests, edge-case tests, and integration tests with CI/CD.

**Indexing or precomputation**  
For larger datasets, introduce indexing (e.g., by direction or lane) to optimize filtering.

**Environment variable management (`.env`)**  
Store future API keys, secrets, or JWT configurations securely.

**Security improvements**  
Introduce authentication, protected routes, and data access controls if scaled to multi-user usage.


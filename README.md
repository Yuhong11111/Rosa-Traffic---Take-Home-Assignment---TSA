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

The FastAPI app serves the health endpoint at `http://localhost:8000/health`.

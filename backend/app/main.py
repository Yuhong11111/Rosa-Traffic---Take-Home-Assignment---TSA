from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import assistant

app = FastAPI(title="Rosa Traffic API")

allowed_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

# configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(assistant.router)


@app.get("/health")
async def health_check():
    """Simple endpoint so the frontend can verify the API is live."""
    return {"status": "ok"}


@app.get("/")
async def root():
    return {"message": "Welcome to Rosa Traffic API"}

from fastapi import FastAPI

app = FastAPI(title="Rosa Traffic API")


@app.get("/health")
async def health_check():
    """Simple endpoint so the frontend can verify the API is live."""
    return {"status": "ok"}


@app.get("/")
async def root():
    return {"message": "Welcome to Rosa Traffic API"}

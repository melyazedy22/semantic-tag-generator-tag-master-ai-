"""
main.py — Entry point.

Run:    uvicorn main:app --reload --port 8000
Docs:   http://localhost:8000/docs
"""

from fastapi import FastAPI
from app.config import settings
from app.api import router

app = FastAPI(
    title="Event Tags AI Agent",
    version="1.0.0",
    description=(
        "Receives an event description and returns AI-generated tags instantly using "
        "LLaMA 3.1 8B (Groq Cloud). Called automatically for every new event."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.include_router(router)


@app.get("/", tags=["Health"], summary="Health Check")
def health():
    return {
        "status":  "ok",
        "model":   settings.groq_model,
        "endpoint": "POST /tags/generate",
    }

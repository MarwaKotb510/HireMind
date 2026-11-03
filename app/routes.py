"""HTTP endpoints."""

from fastapi import APIRouter, HTTPException

from app.config import get_settings
from app.gemini_service import GeminiServiceError, generate_reply
from app.schemas import ChatRequest, ChatResponse, ErrorResponse, HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse, tags=["System"])
def health() -> HealthResponse:
    """Check that the server is running and whether the API key is configured."""
    settings = get_settings()
    return HealthResponse(
        status="ok",
        service="Career Shift Coach backend",
        gemini_key_configured=settings.gemini_api_key is not None,
        gemini_model=settings.gemini_model,
    )


@router.post(
    "/chat",
    response_model=ChatResponse,
    responses={
        422: {"model": ErrorResponse, "description": "Invalid request"},
        429: {"model": ErrorResponse, "description": "AI quota or rate limit"},
        502: {"model": ErrorResponse, "description": "AI service error"},
        503: {"model": ErrorResponse, "description": "AI service unavailable or not configured"},
        504: {"model": ErrorResponse, "description": "AI service timeout"},
    },
    tags=["Chat"],
)
def chat(request: ChatRequest) -> ChatResponse:
    """Send the user's message to Gemini and return the reply.

    Milestone 1: no knowledge base, retrieval, or grounding checks yet.
    """
    settings = get_settings()
    try:
        reply = generate_reply(request.message, settings)
    except GeminiServiceError as error:
        raise HTTPException(status_code=error.status_code, detail=error.detail)
    return ChatResponse(
        reply=reply,
        model=settings.gemini_model,
        grounded_in_knowledge_base=False,
    )
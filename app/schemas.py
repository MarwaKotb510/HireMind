"""Request and response models (Pydantic)."""

from pydantic import BaseModel, Field, field_validator

MAX_MESSAGE_LENGTH = 2000


class ChatRequest(BaseModel):
    message: str = Field(
        ...,
        max_length=MAX_MESSAGE_LENGTH,
        description="The user's message in Arabic or English.",
        examples=["أنا بشتغل في محل بقالة وعايز أتعلم حاجة في الكمبيوتر. أبدأ منين؟"],
    )

    @field_validator("message")
    @classmethod
    def message_must_not_be_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Message must not be empty.")
        return value


class ChatResponse(BaseModel):
    reply: str
    model: str | None = None
    # Honest flag: no knowledge base is connected yet, so this is always False.
    grounded_in_knowledge_base: bool = False


class HealthResponse(BaseModel):
    status: str
    service: str
    gemini_key_configured: bool  # True or False only; the key is never shown
    gemini_model: str


class ErrorResponse(BaseModel):
    detail: str
    # Present only for validation errors: which field failed and why (never the input).
    errors: list[dict[str, str]] | None = None
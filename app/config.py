"""Application settings, loaded from environment variables (.env)."""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()  # reads the .env file in the project root


@dataclass(frozen=True)
class Settings:
    gemini_api_key: str | None
    gemini_model: str
    request_timeout_seconds: int


def _clean(value: str | None) -> str | None:
    """Remove accidental spaces or quotes around a value from .env."""
    if value is None:
        return None
    value = value.strip().strip('"').strip("'").strip()
    return value or None


def get_settings() -> Settings:
    return Settings(
        gemini_api_key=_clean(os.getenv("GEMINI_API_KEY")),
        gemini_model=_clean(os.getenv("GEMINI_MODEL")) or "gemini-3.7-flash",
        request_timeout_seconds=int(os.getenv("REQUEST_TIMEOUT_SECONDS", "30")),
    )
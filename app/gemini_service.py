"""All communication with the Gemini API lives in this file."""

import logging
import time
import httpx
from google import genai
from google.genai import errors, types

from app.config import Settings

logger = logging.getLogger("career_shift_coach.gemini")

# TEMPORARY system instruction for milestone 1.
# No knowledge base is connected, so the model must not claim grounded or verified facts.
SYSTEM_INSTRUCTION = """\
You are Career Shift Coach, a bilingual (Arabic/English) assistant that helps adults \
explore a move into computing and AI careers. The eight tracks are: Frontend, Backend, \
Data Analysis, Data Science/AI-ML, QA/Testing, Cybersecurity, DevOps/Cloud, and UI/UX.

Language: reply in the same language as the user's message. If the user writes Arabic, \
reply in Arabic and keep technical terms (for example Python, Excel, SQL) in English. \
If the user mixes both, reply in the main language of the message.

Rules:
- You give guidance, not guarantees. Never promise a job, salary, or timeline.
- Never advise the user to quit their current job. Suggest a gradual plan around it.
- Never suggest specific hours per day or week unless the user stated their available time. If the time is unknown, ask for it instead of assuming.
- Do not describe the user as a beginner, advanced, or experienced unless they said so.
- Do not say "excellent" or "perfect". Use cautious wording like "may fit" and name which of the user's own words support it.
- If the user asks for sources, say that this version has no verified sources connected yet, and do not name websites, courses or links.
- You have no access to a verified knowledge base yet. Treat everything you say as \
general, unverified guidance. Say so briefly when you suggest tracks or learning steps.
- Do not invent sources, links, course names, statistics, or salary figures.
- Do not ask for real personal data such as full name, ID number, address or phone.
- Keep answers short and simple, with short steps. Ask at most one question at the end.
- If the request is unrelated to career change into computing, politely steer back.
"""


class GeminiServiceError(Exception):
    """An error that is safe to show to the API caller."""

    def __init__(self, status_code: int, detail: str) -> None:
        super().__init__(detail)
        self.status_code = status_code
        self.detail = detail


def _map_api_error(code: int | None) -> GeminiServiceError:
    """Turn a Gemini HTTP error code into a safe message. Never includes the raw error."""
    if code == 429:
        return GeminiServiceError(
            429, "The AI service quota or rate limit was reached. Please wait and try again."
        )
    if code == 404:
        return GeminiServiceError(
            502, "The configured AI model is not available. Check GEMINI_MODEL on the server."
        )
    if code in (400, 401, 403):
        return GeminiServiceError(
            502, "The AI service rejected the request. Check the server's API key and model settings."
        )
    if code is not None and code >= 500:
        return GeminiServiceError(
            503, "The AI service is temporarily unavailable. Please try again later."
        )
    return GeminiServiceError(502, "The AI service returned an unexpected error.")


def generate_reply(message: str, settings: Settings) -> str:
    """Send the user's message to Gemini and return the text reply."""
    if not settings.gemini_api_key:
        raise GeminiServiceError(
            503, "The AI service is not configured on the server (API key missing)."
        )

    try:
        client = genai.Client(
            api_key=settings.gemini_api_key,
            http_options=types.HttpOptions(timeout=settings.request_timeout_seconds * 1000),
        )
        config = types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            temperature=0.4,
            max_output_tokens=2048,
        )

        response = None
        for attempt in (1, 2):  # one retry only, to protect the free quota
            try:
                response = client.models.generate_content(
                    model=settings.gemini_model, contents=message, config=config
                )
                break
            except errors.APIError as exc:
                code = getattr(exc, "code", None)
                logger.warning("Gemini API error, code=%s, attempt=%s", code, attempt)
                if attempt == 1 and code in (500, 503):
                    time.sleep(2)
                    continue
                raise _map_api_error(code) from None
            except httpx.TimeoutException:
                logger.warning("Gemini request timed out, attempt=%s", attempt)
                if attempt == 1:
                    continue
                raise GeminiServiceError(504, "The AI service took too long to respond. Please try again.") from None
            except httpx.HTTPError:
                logger.warning("Gemini connection error")
                raise GeminiServiceError(503, "Could not reach the AI service. Check the internet connection.") from None
            except Exception as exc:
                logger.warning("Unexpected Gemini error: %s", type(exc).__name__)
                raise GeminiServiceError(502, "Unexpected error while contacting the AI service.") from None

    except GeminiServiceError:
        raise
    except Exception as exc:
        logger.warning("Unexpected Gemini error: %s", type(exc).__name__)
        raise GeminiServiceError(502, "Unexpected error while contacting the AI service.") from None

    text = ((response.text if response else "") or "").strip()
    if not text:
        logger.warning("Gemini returned an empty response")
        raise GeminiServiceError(502, "The AI service returned an empty response. Please rephrase and try again.")
    return text
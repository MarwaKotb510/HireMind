"""Creates the FastAPI application."""

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.routes import router

app = FastAPI(
    title="Career Shift Coach Backend",
    description=(
        "First backend milestone: FastAPI + Gemini API. "
        "No knowledge base, retrieval, or grounding checks are implemented yet."
    ),
    version="0.1.0",
)


@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Return readable 422 errors WITHOUT echoing the user's input back."""
    problems = [
        {
            "field": ".".join(str(part) for part in error["loc"] if part != "body"),
            "problem": str(error["msg"]).removeprefix("Value error, "),
        }
        for error in exc.errors()
    ]
    return JSONResponse(
        status_code=422,
        content={"detail": "Invalid request.", "errors": problems},
    )


app.include_router(router)
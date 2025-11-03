from typing import Any, Dict

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


def problem(
    status: int,
    title: str,
    detail: str,
    type_: str = "about:blank",
    correlation_id: str | None = None,
    extras: Dict[str, Any] | None = None,
):
    payload: Dict[str, Any] = {
        "type": type_,
        "title": title,
        "status": status,
        "detail": detail,
    }
    if correlation_id:
        payload["correlation_id"] = correlation_id
    if extras:
        payload.update(extras)
    return JSONResponse(payload, status_code=status)


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    cid = getattr(request.state, "correlation_id", None)
    title = "HTTP Error"
    detail = exc.detail if isinstance(exc.detail, str) else "error"
    return problem(status=exc.status_code, title=title, detail=detail, correlation_id=cid)


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    cid = getattr(request.state, "correlation_id", None)
    return problem(
        status=422,
        title="Validation Error",
        detail="Invalid request",
        correlation_id=cid,
        extras={"errors": exc.errors()},
    )


async def unhandled_exception_handler(request: Request, exc: Exception):
    cid = getattr(request.state, "correlation_id", None)
    return problem(
        status=500,
        title="Internal Server Error",
        detail="An unexpected error occurred",
        correlation_id=cid,
    )



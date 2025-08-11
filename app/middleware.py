import time
import uuid

import structlog
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        rid = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        request.state.request_id = rid
        structlog.contextvars.bind_contextvars(request_id=rid)
        logger = structlog.get_logger()
        start = time.time()
        logger.info("request.start", method=request.method, path=request.url.path)
        response = await call_next(request)
        duration = int((time.time() - start) * 1000)
        response.headers["X-Request-ID"] = rid
        logger.info(
            "request.end",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration_ms=duration,
        )
        structlog.contextvars.clear_contextvars()
        return response


async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"detail": str(exc)})

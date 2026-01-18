from fastapi import Request
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger(__name__)

async def unhandled_exception_handler(request: Request, exc: Exception):
    request_id = getattr(request.state, "request_id", "-")

    logger.exception(
        "Unhandled exception",
        extra={"request_id": request_id},
    )

    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_server_error",
            "message": "Something went wrong. The issue has been logged.",
            "request_id": request_id,
        },
    )

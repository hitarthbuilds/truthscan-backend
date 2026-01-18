import time
import uuid
from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        start_time = time.time()

        # Attach request_id to request state
        request.state.request_id = request_id
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > 5 * 1024 * 1024:
            raise HTTPException(
                status_code=413,
                detail="Payload too large (max 5MB)"
            )

        response = await call_next(request)

        duration = round(time.time() - start_time, 4)

        # Attach headers for observability
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = str(duration)

        return response

import time
from uuid import uuid4

import structlog
from fastapi import Request


logger = structlog.get_logger(__name__)

async def request_logging_middleware(request :Request,call_next):
    """
        Log HTTP request completion with requesti ID

        do not log request Body ,cookies , query parameter ,session , Authorization headers
    """
    structlog.contextvars.clear_contextvars()

    request_id = str(uuid4)

    structlog.contextvars.bind_contextvars(
        request_id = request_id,
        method = request.method,
        path = request.url.path
    )

    start_time = time.perf_counter()
    status_code = 500

    try:
        response = await call_next(request)
        status_code = response.status_code
        response.headers["X-Request-ID"] = request_id

        return response
    finally:
        duration_ms = round((time.perf_counter()-start_time)*1000 ,2)

        if status_code >=500:
            logger.error(
                "http_request_completed",
                status_code = status_code,
                duration_ms = duration_ms
            )

        elif status_code >=400:
            logger.warning(
                "http_request_completed",
                status_code = status_code,
                duration_ms = duration_ms
            )

        else :
            logger.info(
                "http_request_completed",
                status_code = status_code,
                duration_ms = duration_ms
            )

        structlog.contextvars.clear_contextvars()
    
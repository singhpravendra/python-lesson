"""Request context middleware for trace IDs and request logging."""

import logging
import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from utils.id_generator import generate_id
from configs.context import set_trace_id


class RequestContextMiddleware(BaseHTTPMiddleware):
    """Attach trace IDs and log request metrics."""

    def __init__(self, app):
        super().__init__(app)
        self.logger = logging.getLogger("request-logger")

    async def dispatch(self, request: Request, call_next) -> Response:
        trace_id = request.headers.get("x-trace-id") or generate_id()
        set_trace_id(trace_id)

        start_time = time.perf_counter()

        response = await call_next(request)

        duration_ms = (time.perf_counter() - start_time) * 1000

        response.headers["x-trace-id"] = trace_id
        response.headers["x-response-time-ms"] = f"{duration_ms:.2f}"

        client_ip = request.client.host if request.client else "unknown"

        self.logger.info(
            f"{request.method} {request.url.path} "
            f"completed in {duration_ms:.2f} ms with status {response.status_code}",
            extra={
                "method": request.method,
                "path": request.url.path,
                "status": response.status_code,
                "duration_ms": f"{duration_ms:.2f}",
                "client_ip": client_ip,
                "trace_id": trace_id,
            },
        )

        return response

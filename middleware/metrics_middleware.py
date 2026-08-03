import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from metrics.metrics import (
    HTTP_REQUESTS_TOTAL,
    HTTP_REQUEST_DURATION_SECONDS,
    HTTP_REQUESTS_IN_PROGRESS,
)


class MetricsMiddleware(BaseHTTPMiddleware):

    async def dispatch(
        self,
        request: Request,
        call_next,
    ):

        # Do not track Prometheus scraping itself
        if request.url.path == "/metrics":
            return await call_next(request)

        start_time = time.perf_counter()

        HTTP_REQUESTS_IN_PROGRESS.inc()

        status_code = 500

        try:
            response = await call_next(request)

            status_code = response.status_code

            return response

        finally:
            duration = (
                time.perf_counter() - start_time
            )

            HTTP_REQUEST_DURATION_SECONDS.labels(
                method=request.method,
                endpoint=request.url.path,
            ).observe(duration)

            HTTP_REQUESTS_TOTAL.labels(
                method=request.method,
                endpoint=request.url.path,
                status=status_code,
            ).inc()

            HTTP_REQUESTS_IN_PROGRESS.dec()
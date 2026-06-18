import time
import logging

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


logger = logging.getLogger("talentforge")


class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(
        self,
        request: Request,
        call_next
    ):
        start_time = time.perf_counter()

        response = await call_next(request)

        duration = (
            time.perf_counter() - start_time
        ) * 1000

        logger.info(
            f"{request.method} "
            f"{request.url.path} "
            f"Status={response.status_code} "
            f"Duration={duration:.2f}ms"
        )

        return response
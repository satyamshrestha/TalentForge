import logging
import time
import uuid

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from utils.logger import (
    clear_request_id,
    set_request_id,
)


logger = logging.getLogger("talentforge")


class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(
        self,
        request: Request,
        call_next,
    ):
        request_id = str(uuid.uuid4())

        client_ip = (
            request.client.host
            if request.client
            else "unknown"
        )

        token = set_request_id(request_id)
        request.state.request_id = request_id

        start_time = time.perf_counter()

        try:
            response = await call_next(request)

            duration = (
                time.perf_counter() - start_time
            ) * 1000

            response.headers["X-Request-ID"] = request_id

            logger.info(
                "Request completed | "
                "IP=%s | "
                "method=%s | "
                "path=%s | "
                "status=%s | "
                "duration=%.2fms",
                client_ip,
                request.method,
                request.url.path,
                response.status_code,
                duration,
            )

            return response

        except Exception:
            duration = (
                time.perf_counter() - start_time
            ) * 1000

            logger.exception(
                "Request failed | "
                "IP=%s | "
                "method=%s | "
                "path=%s | "
                "duration=%.2fms",
                client_ip,
                request.method,
                request.url.path,
                duration,
            )

            raise

        finally:
            clear_request_id(token)
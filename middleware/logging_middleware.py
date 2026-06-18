import time
import logging
import uuid

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("talentforge")
class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(
        self,
        request: Request,
        call_next
    ):
        client_ip = request.client.host
        request_id = str(uuid.uuid4())[:8]
        start_time = time.perf_counter()
        request.state.request_id = request_id
        try:
            response = await call_next(request)

            duration = (
                time.perf_counter() - start_time
            ) * 1000

            logger.info(
                f"[{request_id}] "
                f"IP={client_ip} "
                f"{request.method} "
                f"{request.url} "
                f"Status={response.status_code} "
                f"Duration={duration:.2f}ms"
            )
            return response

        except Exception:
            duration = (
                time.perf_counter() - start_time
            ) * 1000

            logger.exception(
                f"[{request_id}] "
                f"IP={client_ip} "
                f"{request.method} "
                f"{request.url} "
                f"FAILED "
                f"Duration={duration:.2f}ms"
            )
            raise
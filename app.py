import logging

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

import models
from api.v1.api import api_router
from exceptions.app_exception import AppException
from middleware.logging_middleware import LoggingMiddleware
from middleware.security_headers import SecurityHeadersMiddleware
from middleware.rate_limit import limiter
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from utils.config import settings
from utils.logger import configure_logging


configure_logging()

logger = logging.getLogger("talentforge")


@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info(
        "Starting %s v%s",
        settings.APP_NAME,
        settings.APP_VERSION,
    )

    yield

    logger.info(
        "Stopping %s",
        settings.APP_NAME,
    )


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered interview preparation platform.",
    lifespan=lifespan,
)


app.state.limiter = limiter


app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=[
        "GET",
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
    ],
    allow_headers=[
        "Authorization",
        "Content-Type",
    ],
)


app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS,
)


app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(LoggingMiddleware)


app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler,
)


app.include_router(
    api_router,
    prefix="/api/v1",
)


@app.exception_handler(AppException)
async def app_exception_handler(
    request,
    exc: AppException,
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
        },
    )


@app.get(
    "/",
    tags=["Health"],
)
def home():
    return {
        "name": settings.APP_NAME,
        "status": "running",
        "version": settings.APP_VERSION,
    }
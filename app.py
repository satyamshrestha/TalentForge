from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

import models
import utils.logger
from api.v1.api import api_router
from exceptions.app_exception import AppException
from middleware.logging_middleware import LoggingMiddleware
from middleware.security_headers import SecurityHeadersMiddleware
from middleware.rate_limit import limiter
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from utils.config import settings

app = FastAPI()
app.state.limiter = limiter

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=[
        "localhost",
        "127.0.0.1",
        "*.localhost",
    ]
)

app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(LoggingMiddleware)

app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)

app.include_router(api_router, prefix="/api/v1")

@app.exception_handler(AppException)
async def app_exception_handler(
    request,
    exc: AppException,
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail
        }
    )

@app.get("/")
def home():
    return {"message": "Welcome to TalentForge!"}
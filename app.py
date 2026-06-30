from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

import models
import utils.logger
from api.v1.api import api_router
from middleware.logging_middleware import LoggingMiddleware
from utils.config import settings

app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY
)

app.add_middleware(LoggingMiddleware)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def home():
    return {"message": "Welcome to TalentForge!"}
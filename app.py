from fastapi import FastAPI

import models
import utils.logger
from api.v1.api import api_router
from middleware.logging_middleware import LoggingMiddleware

app = FastAPI()
app.include_router(api_router, prefix="/api/v1")
app.add_middleware(LoggingMiddleware)

@app.get("/")
def home():
    return {"message": "Welcome to TalentForge!"}
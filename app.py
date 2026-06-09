from fastapi import FastAPI

import models
from api.v1.api import api_router

app = FastAPI()
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def home():
    return {"message": "Welcome to TalentForge!"}
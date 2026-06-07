from fastapi import APIRouter

from routers import auth_router, resume_router

api_router = APIRouter()

api_router.include_router(auth_router.router)
api_router.include_router(resume_router.router)
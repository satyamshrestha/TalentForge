from fastapi import APIRouter

from routers import auth_router, resume_router, interview_router, answer_router, dashboard_router

api_router = APIRouter()

api_router.include_router(auth_router.router)
api_router.include_router(resume_router.router)
api_router.include_router(interview_router.router)
api_router.include_router(answer_router.router)
api_router.include_router(dashboard_router.router)
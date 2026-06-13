from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from models.user import User
from db.deps import get_db
from auth.deps import get_current_user
from services.interview_service import InterviewService
from services.deps import get_interview_service
from schemas.interview_schema import InterviewResponse, InterviewListReponse, InterviewDetailResponse

router = APIRouter(prefix="/interviews", tags=["Interview"])

@router.post("/from-resume/{resume_id}", response_model=InterviewResponse)
def create_interview(
    resume_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    service: InterviewService = Depends(get_interview_service),
):
    return service.create_interview_from_resume(db, resume_id, current_user)

@router.get("", response_model=list[InterviewListReponse])
def get_user_interviews(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    service: InterviewService = Depends(get_interview_service)
):
    return service.get_user_interviews(db, current_user)

@router.get("/{interview_id}", response_model=InterviewDetailResponse)
def get_interview_detail(
    interview_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    service: InterviewService = Depends(get_interview_service)
):
    return service.get_interview_detail(db, interview_id, current_user)
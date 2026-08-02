from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from auth.scope_deps import require_scope
from models.user import User
from db.deps import get_db
from services.interview_service import InterviewService
from services.deps import get_interview_service
from schemas.interview_schema import (
    InterviewResponse,
    InterviewPaginationResponse,
    InterviewDetailResponse,
    InterviewSummaryResponse,
    MessageResponse,
)


router = APIRouter(
    prefix="/interviews",
    tags=["Interviews"],
    responses={
        401: {
            "description": "Authentication required"
        },
        403: {
            "description": "Missing required permission scope"
        },
    },
)


@router.post(
    "/from-resume/{resume_id}",
    response_model=InterviewResponse,
    summary="Create interview from resume",
    description=(
        "Creates a new interview session based on "
        "the selected resume. Requires the "
        "interview:create permission scope."
    ),
)
def create_interview(
    resume_id: str,
    current_user: User = Depends(require_scope("interview:create")),
    db: Session = Depends(get_db),
    service: InterviewService = Depends(get_interview_service),
):
    return service.create_interview_from_resume(
        db,
        resume_id,
        current_user,
    )


@router.post(
    "/{interview_id}/retake",
    response_model=InterviewResponse,
    summary="Retake interview",
    description=(
        "Creates a new interview attempt from an existing "
        "interview. Requires the interview:read permission scope."
    ),
)
def retake_interview(
    interview_id: str,
    current_user: User = Depends(require_scope("interview:read")),
    db: Session = Depends(get_db),
    service: InterviewService = Depends(get_interview_service),
):
    return service.retake_interview(
        db,
        interview_id,
        current_user,
    )


@router.get(
    "/my_interviews",
    response_model=InterviewPaginationResponse,
    summary="Get user interviews",
    description=(
        "Returns paginated interview history for "
        "the authenticated user."
    ),
)
def get_user_interviews(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    status: str | None = None,
    current_user: User = Depends(require_scope("interview:read")),
    db: Session = Depends(get_db),
    service: InterviewService = Depends(get_interview_service),
):
    return service.get_user_interviews(
        db,
        current_user,
        page,
        size,
        status,
    )


@router.get(
    "/{interview_id}/summary",
    response_model=InterviewSummaryResponse,
    summary="Get interview summary",
    description=(
        "Returns a summary of a completed interview "
        "including evaluation results."
    ),
)
def get_interview_summary(
    interview_id: str,
    current_user: User = Depends(require_scope("interview:read")),
    db: Session = Depends(get_db),
    service: InterviewService = Depends(get_interview_service),
):
    return service.get_interview_summary(
        db,
        interview_id,
        current_user,
    )


@router.get(
    "/{interview_id}",
    response_model=InterviewDetailResponse,
    summary="Get interview details",
    description=(
        "Returns detailed information about a specific "
        "interview session."
    ),
)
def get_interview_detail(
    interview_id: str,
    current_user: User = Depends(require_scope("interview:read")),
    db: Session = Depends(get_db),
    service: InterviewService = Depends(get_interview_service),
):
    return service.get_interview_detail(
        db,
        interview_id,
        current_user,
    )


@router.delete(
    "/{interview_id}",
    response_model=MessageResponse,
    summary="Delete interview",
    description=(
        "Deletes an interview session belonging to "
        "the authenticated user. Requires the "
        "interview:delete permission scope."
    ),
)
def delete_interview(
    interview_id: str,
    current_user: User = Depends(require_scope("interview:delete")),
    db: Session = Depends(get_db),
    service: InterviewService = Depends(get_interview_service),
):
    return service.delete_interview(
        db,
        interview_id,
        current_user,
    )
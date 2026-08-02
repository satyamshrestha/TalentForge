from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from auth.scope_deps import require_scope
from db.deps import get_db
from models.user import User
from schemas.answer_schema import AnswerCreate, AnswerResponse
from services.answer_service import AnswerService
from services.deps import get_answer_service


router = APIRouter(
    prefix="/answers",
    tags=["Answers"],
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
    "",
    response_model=AnswerResponse,
    summary="Submit interview answer",
    description=(
        "Submits an answer for an interview question. "
        "The answer can later be evaluated by the AI "
        "analysis pipeline. Requires the "
        "answer:create permission scope."
    ),
)
def submit_answer(
    payload: AnswerCreate,
    current_user: User = Depends(require_scope("answer:create")),
    db: Session = Depends(get_db),
    service: AnswerService = Depends(get_answer_service),
):
    return service.submit_answer(
        db,
        payload.question_id,
        payload.answer_text,
    )
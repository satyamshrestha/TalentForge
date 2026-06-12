from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from auth.deps import get_current_user
from db.deps import get_db
from models.user import User
from services.answer_service import AnswerService
from services.deps import get_answer_service
from schemas.answer_schema import AnswerCreate, AnswerResponse

router = APIRouter(prefix="/answers", tags=["Answers"])

@router.post("", response_model=AnswerResponse)
def submit_answer(
    payload: AnswerCreate,
    db: Session = Depends(get_db),
    service: AnswerService = Depends(get_answer_service)
):
    return service.submit_answer(db, payload.question_id, payload.answer_text)
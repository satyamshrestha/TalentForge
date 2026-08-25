from sqlalchemy.orm import Session

from models.interview import Interview
from models.question import Question


def can_access_interview(
    db: Session,
    user_id: str,
    interview_id: str,
) -> bool:
    interview = (
        db.query(Interview)
        .filter(
            Interview.id == interview_id,
            Interview.user_id == user_id,
        )
        .first()
    )

    return interview is not None


def can_access_question(
    db: Session,
    user_id: str,
    interview_id: str,
    question_id: str,
) -> bool:
    question = (
        db.query(Question)
        .filter(Question.id == question_id)
        .first()
    )

    if not question:
        return False

    interview = question.interview

    if not interview:
        return False

    return (
        interview.id == interview_id
        and interview.user_id == user_id
    )
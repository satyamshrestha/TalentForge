from sqlalchemy.orm import Session

from models.interview import Interview


def can_access_interview(
    db: Session,
    user_id: str,
    interview_id: str,
) -> bool:
    interview = (
        db.query(Interview)
        .filter(Interview.id == interview_id)
        .first()
    )

    if not interview:
        return False

    return interview.user_id == user_id
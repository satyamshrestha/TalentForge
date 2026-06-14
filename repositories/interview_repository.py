from sqlalchemy.orm import Session

from models.interview import Interview

class InterviewRepository:

    def create_interview(
        self,
        db: Session,
        interview: Interview
    ):
        db.add(interview)
        db.commit()
        db.refresh(interview)
        return interview
    
    def get_interview_by_id(
        self,
        db: Session,
        id: str
    ):
        return (db.query(Interview).filter(Interview.id == id).first())
    
    def get_interview_by_user_id(
        self,
        db: Session,
        user_id: str
    ):
        return (db.query(Interview).filter(Interview.user_id==user_id).all())

    def update_interview_status(
        self,
        db: Session,
        interview: Interview,
        status: str
    ):
        interview.status = status
        db.commit()
        db.refresh(interview)
        return interview
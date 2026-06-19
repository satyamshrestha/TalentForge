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
    
    def get_interviews(
        self, 
        db: Session, 
        user_id: str, 
        page: int, 
        size: int, 
        status: str | None=None
    ):
        query = (db.query(Interview).filter(Interview.user_id == user_id))
        if status:
            query = query.filter(Interview.status == status)
        offset = (page-1)*size
        query = query.order_by(Interview.created_at.desc())
        return (
            query
            .offset(offset)
            .limit(size)
            .all()
        )

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
    
    def delete_interview(
        self,
        db: Session,
        interview: Interview
    ):
        db.delete(interview)
        db.commit()
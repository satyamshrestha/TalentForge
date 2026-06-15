from sqlalchemy.orm import Session

from models.resume import Resume
from models.interview import Interview

class DashboardRepository:
    def get_total_resumes(
        self,
        db: Session,
        user_id: str
    ):
        return (db.query(Resume).filter(Resume.user_id==user_id).count())
    
    def get_total_interviews(
        self,
        db: Session,
        user_id: str
    ):
        return (db.query(Interview).filter(Interview.user_id==user_id).count())
    
    def get_completed_interviews(
        self,
        db: Session,
        user_id: str
    ):
        return (
            db.query(Interview)
            .filter(
                Interview.user_id==user_id,
                Interview.status=="COMPLETED"
            )
            .count()
        )
    
    def get_recent_interviews(
        self,
        db: Session,
        user_id: str
    ):
        return (
            db.query(Interview)
            .filter(Interview.user_id==user_id)
            .order_by(Interview.created_at.desc())
            .limit(5)
            .all()
        )
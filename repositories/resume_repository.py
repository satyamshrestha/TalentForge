from sqlalchemy.orm import Session

from models.resume import Resume

class ResumeRepository:

    def create_resume(
        self, 
        db: Session,
        resume: Resume
    ):
        db.add(resume)
        db.commit()
        db.refresh(resume)
        return resume
    
    def get_all_resumes_by_user(
        self,
        db: Session,
        user_id: str
    ):
        return (db.query(Resume).filter(Resume.user_id==user_id).all())
    
    def get_resume_by_id(
        self,
        db: Session,
        id: str
    ):
        return (db.query(Resume).filter(Resume.id == id).first())
    
    def persist(
        self,
        db: Session,
        resume: Resume
    ):
        db.commit()
        db.refresh(resume)
        return resume
    
    def delete_resume(
        self,
        db: Session,
        resume: Resume
    ):
        db.delete(resume)
        db.commit()
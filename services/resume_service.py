import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException

from models.resume import Resume
from models.user import User
from repositories.resume_repository import ResumeRepository

class ResumeService:
    def __init__(
        self,
        repository: ResumeRepository
    ):
        self.repository = repository

    def create_resume(
        self,
        db: Session,
        current_user: User,
        file_url: str,
        parsed_text: str
    ):
        resume = Resume(
            id=str(uuid.uuid4()),
            file_url=file_url,
            parsed_text=parsed_text,
            user_id=current_user.id
        )
        return self.repository.create_resume(db, resume)
    
    def get_resume(
        self,
        db: Session,
        id: str,
        current_user: User
    ):
        return self._get_owned_resume(db, id, current_user.id)

    def get_my_resumes(
        self,
        db: Session,
        current_user: User
    ):
        return self.repository.get_all_resumes_by_user(db, current_user.id)
    
    def update_resume(
        self,
        db: Session,
        id: str,
        current_user: User,
        file_url: str,
        parsed_text: str
    ):
        resume = self._get_owned_resume(db, id, current_user)
        resume.file_url = file_url
        resume.parsed_text = parsed_text
        return self.repository.persist(db, resume)
    
    def delete_resume(
        self,
        db: Session,
        id: str,
        current_user: User
    ):
        resume = self._get_owned_resume(db, id, current_user)
        self.repository.delete_resume(db, resume)       
        return True

    def _get_owned_resume(
        self,
        db: Session,
        id: str,
        current_user: User
    ):
        resume = self.repository.get_resume_by_id(db, id)
        if not resume:
            raise HTTPException(status_code=404, detail="Resume does not exist!")
        if resume.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Resume does not belong to the current user!")
        return resume

import json
import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException

from db.redis import redis_client
from models.resume import Resume
from models.user import User
from repositories.resume_repository import ResumeRepository
from tasks import process_resume

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
        resume = self.repository.create_resume(db, resume)
        cache_key = self._get_resume_cache_key(current_user.id)
        redis_client.delete(cache_key)
        process_resume.delay(resume.id)
        return resume
    
    def get_resume(
        self,
        db: Session,
        id: str,
        current_user: User
    ):
        return self._get_owned_resume(db, id, current_user)

    def get_my_resumes(
        self,
        db: Session,
        current_user: User
    ):
        cache_key = self._get_resume_cache_key(current_user.id)
        cached = redis_client.get(cache_key)
        if cached is not None:
            return json.loads(cached)
        resumes = self.repository.get_all_resumes_by_user(db, current_user.id)
        resume_data = [
            {
                "id": resume.id, 
                "file_url": resume.file_url, 
                "parsed_text": resume.parsed_text, 
                "user_id": resume.user_id
            }
            for resume in resumes
        ]
        redis_client.set(
            cache_key,
            json.dumps(resume_data),
            ex=300
        )
        return resume_data
    
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
        resume = self.repository.persist(db, resume)
        cache_key = self._get_resume_cache_key(current_user.id)
        redis_client.delete(cache_key)
        return resume
    
    def delete_resume(
        self,
        db: Session,
        id: str,
        current_user: User
    ):
        resume = self._get_owned_resume(db, id, current_user)
        self.repository.delete_resume(db, resume)
        cache_key = self._get_resume_cache_key(current_user.id)
        redis_client.delete(cache_key)       
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

    def _get_resume_cache_key(
        self,
        user_id: str
    ):
        return f"user:{user_id}:resumes"
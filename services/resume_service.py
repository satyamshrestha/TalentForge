import json, uuid, os
from sqlalchemy.orm import Session
from fastapi import UploadFile

from db.redis import redis_client
from models.user import User
from models.resume import Resume
from exceptions.resume_exception import (
    InvalidResumeFileException,
    ResumeAccessDeniedException,
    ResumeNotFoundException
)
from tasks.resume_tasks import process_resume
from repositories.resume_repository import ResumeRepository

class ResumeService:
    def __init__(
        self,
        repository: ResumeRepository
    ):
        self.repository = repository

    def upload_resume(
        self,
        db: Session,
        current_user: User,
        file: UploadFile
    ):
        if file.content_type != "application/pdf":
            raise InvalidResumeFileException()
        file_name = f"{str(uuid.uuid4())}_{file.filename}"
        file_path = os.path.join(
            "uploads",
            "resumes",
            file_name
        )
        os.makedirs(
            os.path.dirname(file_path),
            exist_ok=True
        )
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())
        resume = Resume(
            id=str(uuid.uuid4()),
            file_path=file_path,
            status="PENDING",
            user_id=current_user.id
        )
        resume = self.repository.create_resume(db, resume)
        cache_key = self._get_resume_cache_key(current_user.id)
        redis_client.delete(cache_key)
        process_resume.delay(resume.id)
        return resume
    
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
                "file_path": resume.file_path, 
                "parsed_text": resume.parsed_text, 
                "status": resume.status,
                "error_message": resume.error_message,
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

    def get_resume(
        self,
        db: Session,
        id: str,
        current_user: User
    ):
        return self._get_owned_resume(db, id, current_user)
    
    def delete_resume(
        self,
        db: Session,
        id: str,
        current_user: User
    ):
        resume = self._get_owned_resume(db, id, current_user)
        if os.path.exists(resume.file_path):
            os.remove(resume.file_path)
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
            raise ResumeNotFoundException()
        if resume.user_id != current_user.id:
            raise ResumeAccessDeniedException()
        return resume

    def _get_resume_cache_key(
        self,
        user_id: str
    ):
        return f"user:{user_id}:resumes"
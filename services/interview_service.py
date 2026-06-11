import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException

from models.user import User
from models.interview import Interview
from models.question import Question
from repositories.interview_repository import InterviewRepository
from repositories.resume_repository import ResumeRepository
from services.question_generator import QuestionGenerator

class InterviewService:

    def __init__(
        self,
        interview_repository: InterviewRepository,
        resume_repository: ResumeRepository,
        question_generator: QuestionGenerator        
    ):
        self.interview_repository = interview_repository
        self.resume_repository = resume_repository
        self.question_generator = question_generator

    def create_interview_from_resume(
        self,
        db: Session,
        resume_id: str,
        current_user: User
    ):
        resume = self.resume_repository.get_resume_by_id(db, resume_id)
        if not resume:
            raise HTTPException(status_code=404, detail="Resume not found!")
        if resume.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Resume doesn't belong to the current user.")
        
        analysis = (resume.parsed_text or {}).get("analysis", {})
        skills = analysis.get("backend_skills", [])
        if not skills:
            raise HTTPException(status_code=404, detail="No backend skills found in resume.")
        questions = self.question_generator.generate(skills)

        interview = Interview(
            id=str(uuid.uuid4()),
            role_target="Backend Engineer",
            status="CREATED",
            user_id=current_user.id
        )
        interview = self.interview_repository.create_interview(db, interview)

        for question_text in questions:
            question = Question(
                id=str(uuid.uuid4()),
                question_text=question_text,
                interview_id=interview.id
            )
            self.interview_repository.create_question(db, question)
            
        return self.interview_repository.get_interview_by_id(db, interview.id)

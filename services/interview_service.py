import math
import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException

from models.user import User
from models.interview import Interview
from models.question import Question
from repositories.interview_repository import InterviewRepository
from repositories.question_repository import QuestionRepository
from repositories.resume_repository import ResumeRepository
from services.audit_log_service import AuditLogService
from services.question_generator import QuestionGenerator

class InterviewService:

    def __init__(
        self,
        interview_repository: InterviewRepository,
        question_repository: QuestionRepository,
        resume_repository: ResumeRepository,
        question_generator: QuestionGenerator,
        audit_log_service: AuditLogService       
    ):
        self.interview_repository = interview_repository
        self.question_repository = question_repository
        self.resume_repository = resume_repository
        self.question_generator = question_generator
        self.audit_log_service = audit_log_service

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
            raise HTTPException(status_code=400, detail="No backend skills found in resume.")
        questions = self.question_generator.generate(skills)

        interview = Interview(
            id=str(uuid.uuid4()),
            role_target="Backend Engineer",
            status="CREATED",
            user_id=current_user.id
        )
        interview = self.interview_repository.create_interview(db, interview)
        self.audit_log_service.log_action(
            db,
            current_user.id,
            "CREATE_INTERVIEW",
            "INTERVIEW",
            interview.id
        )

        for question_text in questions:
            question = Question(
                id=str(uuid.uuid4()),
                question_text=question_text,
                interview_id=interview.id
            )
            self.question_repository.create_question(db, question)
            
        return self.interview_repository.get_interview_by_id(db, interview.id)
    
    def retake_interview(
        self,
        db: Session,
        interview_id: str,
        current_user: User
    ):
        original_interview = self._accessible_interview(db, interview_id, current_user)
        new_interview = Interview(
            id=str(uuid.uuid4()),
            role_target=original_interview.role_target,
            status="CREATED",
            user_id=current_user.id
        )
        new_interview = self.interview_repository.create_interview(db, new_interview)
        self.audit_log_service.log_action(
            db,
            current_user.id,
            "RETAKE_INTERVIEW",
            "INTERVIEW",
            new_interview.id
        )
        
        for old_question in original_interview.questions:
            question = Question(
                id=str(uuid.uuid4()),
                question_text=old_question.question_text,
                interview_id=new_interview.id
            )
            self.question_repository.create_question(db, question)
        return self.interview_repository.get_interview_by_id(db, new_interview.id)
    
    def get_user_interviews(
        self,
        db: Session,
        current_user: User,
        page: int = 1,
        size: int = 10,
        status: str | None = None
    ):
        result = self.interview_repository.get_interviews(db, current_user.id, page, size, status)
        return {
            "items": result["items"],
            "page": page,
            "size": size,
            "total": result["total"],
            "pages": math.ceil(
                result["total"] / size
                if result["total"]
                else 1
            )
        }
    
    def get_interview_detail(
        self,
        db: Session,
        interview_id: str,
        current_user: User
    ):
        interview = self._accessible_interview(db, interview_id, current_user)
        statistics = self._build_interview_statistics(interview)
        return {
            "id": interview.id,
            "role_target": interview.role_target,
            "status": interview.status,
            "created_at": interview.created_at,
            "statistics": statistics,
            "questions": interview.questions
        }
    
    def get_interview_summary(
        self,
        db: Session,
        interview_id: str,
        current_user: User
    ):
        interview = self._accessible_interview(db, interview_id, current_user)
        statistics = self._build_interview_statistics(interview)
        feedbacks = [
            question.answer.feedback
            for question in interview.questions
            if question.answer
        ]           # Future enhancement: Use feedbacks to generate more detailed strengths/weaknesses.

        strengths = []
        weaknesses = []
        if statistics["average_score"] >= 8:
            strengths.append("Strong overall interview performance.")
        elif statistics["average_score"] >= 6:
            strengths.append("Good backend fundamentals.")
        else:
            weaknesses.append("Needs improvement in core backend concepts.")
        
        if statistics["average_score"] >= 8:
            overall_feedback = ("Strong backend knowledge demonstrated.")

        elif statistics["average_score"] >= 6:
            overall_feedback = ("Good understanding with room for improvement.")

        else:
            overall_feedback = ("Further practice is recommended.")

        return {
            "interview_id": interview.id,
            "created_at": interview.created_at,
            "average_score": statistics["average_score"],
            "total_questions": statistics["total_questions"],
            "answered_questions": statistics["answered_questions"],
            "strengths": strengths,
            "weaknesses": weaknesses,
            "overall_feedback": overall_feedback
        }
    
    def delete_interview(
        self,
        db: Session,
        interview_id: str,
        current_user: User
    ):
        interview = self._accessible_interview(
            db,
            interview_id,
            current_user
        )
        self.audit_log_service.log_action(
            db,
            current_user.id,
            "DELETE_INTERVIEW",
            "INTERVIEW",
            interview.id
        )
        self.interview_repository.delete_interview(db, interview)
        return {"message": "Interview deleted successfully."}
    
    def _build_interview_statistics(
        self,
        interview: Interview
    ):
        total_questions = len(interview.questions)
        answered_questions = sum(
            1
            for question in interview.questions
            if question.answer
        )
        scores = [
            int(question.answer.score)
            for question in interview.questions
            if question.answer
        ]
        average_score = (
            sum(scores)/len(scores)
            if scores
            else 0
        )
        
        completion_percentage = (
            (answered_questions/total_questions) * 100
            if total_questions
            else 0
        )
        return {
            "total_questions": total_questions,
            "answered_questions": answered_questions,
            "average_score": round(average_score, 2),
            "completion_percentage": round(completion_percentage, 2)
        }
    
    def _accessible_interview(
        self,
        db: Session,
        interview_id: str,
        current_user: User
    ):
        interview = self.interview_repository.get_interview_by_id(db, interview_id)
        if not interview:
            raise HTTPException(status_code=404, detail="Interview not found!")
        if interview.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Access Denied!")
        return interview
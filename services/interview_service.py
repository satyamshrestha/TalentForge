import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException

from models.user import User
from models.interview import Interview
from models.question import Question
from repositories.interview_repository import InterviewRepository
from repositories.question_repository import QuestionRepository
from repositories.resume_repository import ResumeRepository
from services.question_generator import QuestionGenerator

class InterviewService:

    def __init__(
        self,
        interview_repository: InterviewRepository,
        question_repository: QuestionRepository,
        resume_repository: ResumeRepository,
        question_generator: QuestionGenerator        
    ):
        self.interview_repository = interview_repository
        self.question_repository = question_repository
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
            raise HTTPException(status_code=400, detail="No backend skills found in resume.")
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
            self.question_repository.create_question(db, question)
            
        return self.interview_repository.get_interview_by_id(db, interview.id)
    
    def get_user_interviews(
        self,
        db: Session,
        current_user: User
    ):
        return self.interview_repository.get_interview_by_user_id(db, current_user.id)
    
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
            "average_score": statistics["average_score"],
            "total_questions": statistics["total_questions"],
            "answered_questions": statistics["answered_questions"],
            "strengths": strengths,
            "weaknesses": weaknesses,
            "overall_feedback": overall_feedback
        }
    
    
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
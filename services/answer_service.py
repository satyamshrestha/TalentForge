import uuid
from sqlalchemy.orm import Session

from exceptions.answer_exception import QuestionAlreadyAnsweredException
from exceptions.question_exception import QuestionNotFoundException
from ai.services.answer_evaluator import AnswerEvaluator
from models.answer import Answer
from repositories.answer_repository import AnswerRepository
from repositories.interview_repository import InterviewRepository
from repositories.question_repository import QuestionRepository
from services.audit_log_service import AuditLogService

class AnswerService:

    def __init__(
        self,
        answer_repository: AnswerRepository,
        answer_evaluator: AnswerEvaluator,
        question_repository: QuestionRepository,
        interview_repository: InterviewRepository,
        audit_log_service: AuditLogService
    ):
        self.answer_repository = answer_repository
        self.answer_evaluator = answer_evaluator
        self.question_repository = question_repository
        self.interview_repository = interview_repository
        self.audit_log_service = audit_log_service

    def submit_answer(
        self,
        db: Session,
        question_id: str,
        answer_text: str
    ):
        question = self.question_repository.get_question_by_id(db, question_id)
        if not question:
            raise QuestionNotFoundException()
        
        existing_answer = self.answer_repository.get_answer_by_question_id(db, question_id)
        if existing_answer:
            raise QuestionAlreadyAnsweredException()
        
        evaluation = self.answer_evaluator.evaluate(
            question.question_text,
            answer_text
        )

        answer = Answer(
            id=str(uuid.uuid4()),
            answer_text=answer_text,
            feedback=evaluation.feedback,
            score=evaluation.score,
            suggested_improvement=evaluation.suggested_improvement,
            question_id=question.id
        )
        answer = self.answer_repository.create_answer(db, answer)
        self.audit_log_service.log_action(
            db,
            question.interview.user_id,
            "SUBMIT_ANSWER",
            "QUESTION",
            question.id
        )
        interview = question.interview
        total_questions = len(interview.questions)
        answered_questions = sum(
            1
            for question in interview.questions
            if question.answer
        )
        if answered_questions == total_questions:
            status = "COMPLETED"
        else:
            status = "IN_PROGRESS"

        self.interview_repository.update_interview_status(db, interview, status)
        return answer
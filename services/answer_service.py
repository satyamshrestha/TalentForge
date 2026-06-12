import uuid
from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.answer import Answer
from services.answer_evaluator import AnswerEvaluator
from repositories.answer_repository import AnswerRepository
from repositories.question_repository import QuestionRepository

class AnswerService:

    def __init__(
        self,
        answer_repository: AnswerRepository,
        answer_evaluator: AnswerEvaluator,
        question_repository: QuestionRepository
    ):
        self.answer_repository = answer_repository
        self.answer_evaluator = answer_evaluator
        self.question_repository = question_repository

    def submit_answer(
        self,
        db: Session,
        question_id: str,
        answer_text: str
    ):
        question = self.question_repository.get_question_by_id(db, question_id)
        if not question:
            raise HTTPException(status_code=404, detail="Question doesn't exist!")
        
        existing_answer = self.answer_repository.get_answer_by_question_id(db, question_id)
        if existing_answer:
            raise HTTPException(status_code=400, detail="Question already answered.")
        
        evaluation = self.answer_evaluator.evaluate(question.question_text, answer_text)
        
        answer = Answer(
            id=str(uuid.uuid4()),
            answer_text=answer_text,
            feedback=evaluation["feedback"],
            score=str(evaluation["score"]),
            question_id=question.id
        )
        return self.answer_repository.create_answer(db, answer)
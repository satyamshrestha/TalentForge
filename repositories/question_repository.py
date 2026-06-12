from sqlalchemy.orm import Session

from models.question import Question

class QuestionRepository:

    def create_question(
        self,
        db: Session,
        question: Question
    ):
        db.add(question)
        db.commit()
        db.refresh(question)
        return question

    def get_question_by_id(
        self,
        db: Session,
        id: str
    ):
        return (db.query(Question).filter(Question.id == id).first())
from sqlalchemy.orm import Session

from models.answer import Answer

class AnswerRepository:

    def create_answer(
        self,
        db: Session,
        answer: Answer
    ):
        db.add(answer)
        db.commit()
        db.refresh(answer)
        return answer

    def get_answer_by_id(
        self,
        db: Session,
        id: str
    ):
        return (db.query(Answer).filter(Answer.id == id).first())

    def get_answer_by_question_id(
        self,
        db: Session,
        question_id: str
    ):
        return (db.query(Answer).filter(Answer.question_id == question_id).first())
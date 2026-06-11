from sqlalchemy.orm import Session

from models.interview import Interview
from models.question import Question

class InterviewRepository():

    def create_interview(
        self,
        db: Session,
        interview: Interview
    ):
        db.add(interview)
        db.commit()
        db.refresh(interview)
        return interview

    def create_question(
        self,
        db: Session,
        question: Question
    ):
        db.add(question)
        db.commit()
        db.refresh(question)
        return question
    
    def get_interview_by_id(
        self,
        db: Session,
        id: str
    ):
        return (db.query(Interview).filter(Interview.id == id).first())
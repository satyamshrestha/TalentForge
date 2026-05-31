from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from db.database import Base

class Question(Base):
    __tablename__ = "questions"
    id = Column(String, primary_key=True)
    question_text = Column(String)
    interview_id = Column(
        String,
        ForeignKey("interviews.id")
    )
    interview = relationship(
        "Interview",
        back_populates="questions"
    )
    answer = relationship(
        "Answer",
        back_populates="question",
        uselist=False           # One question --> One answer NOT One question --> Many answer
    )
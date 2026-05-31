from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from db.database import Base


class Answer(Base):
    __tablename__ = "answers"
    id = Column(String, primary_key=True)
    answer_text = Column(String)
    feedback = Column(String)
    score = Column(String)
    question_id = Column(
        String,
        ForeignKey("questions.id")
    )
    question = relationship(
        "Question",
        back_populates="answer"
    )
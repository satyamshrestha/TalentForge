from pydantic import BaseModel, ConfigDict


class AnswerCreate(BaseModel):
    question_id: str
    answer_text: str

class AnswerResponse(BaseModel):
    id: str
    answer_text: str
    feedback: str
    score: int
    suggested_improvement: str | None
    question_id: str

    class Config:
        from_attributes = True
from pydantic import BaseModel


class AnswerCreate(BaseModel):
    question_id: str
    answer_text: str

class AnswerResponse(BaseModel):
    id: str
    answer_text: str
    feedback: str
    score: str

    class Config:
        from_attributes=True
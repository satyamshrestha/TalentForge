from pydantic import BaseModel, ConfigDict


class AnswerCreate(BaseModel):
    question_id: str
    answer_text: str

class AnswerResponse(BaseModel):
    id: str
    answer_text: str
    feedback: str
    score: str

    model_config = ConfigDict(
        from_attributes=True
    )
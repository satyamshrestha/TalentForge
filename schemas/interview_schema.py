from pydantic import BaseModel

class QuestionResponse(BaseModel):
    id: str
    question_text: str

    class Config:
        from_attributes = True

class InterviewResponse(BaseModel):
    id: str
    role_target: str | None
    status: str
    questions: list[QuestionResponse]

    class Config:
        from_attributes = True
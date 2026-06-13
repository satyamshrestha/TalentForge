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

class InterviewListReponse(BaseModel):
    id: str
    role_target: str | None
    status: str

    class Config:
        from_attributes = True

class AnswerDetailResponse(BaseModel):
    id: str
    score: str
    feedback: str

    class Config:
        from_attributes = True

class QuestionDetailResponse(BaseModel):
    id: str
    question_text: str
    answer: AnswerDetailResponse | None = None

    class Config:
        from_attributes = True

class InterviewStatisticsResponse(BaseModel):
    total_questions: int
    answered_questions: int
    average_score: float
    completion_percentage: float

class InterviewDetailResponse(BaseModel):
    id: str
    role_target: str
    status: str
    statistics: InterviewStatisticsResponse
    questions: list[QuestionDetailResponse]

    class Config:
        from_attributes = True
from datetime import datetime
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
    created_at: datetime
    questions: list[QuestionResponse]

    class Config:
        from_attributes = True

class InterviewListResponse(BaseModel):
    id: str
    role_target: str | None
    status: str
    created_at: datetime

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
    created_at: datetime
    statistics: InterviewStatisticsResponse
    questions: list[QuestionDetailResponse]

    class Config:
        from_attributes = True

class InterviewSummaryResponse(BaseModel):
    interview_id: str
    created_at: datetime
    average_score: float
    total_questions: int
    answered_questions: int
    strengths: list[str]
    weaknesses: list[str]
    overall_feedback: str

class MessageResponse(BaseModel):
    message: str
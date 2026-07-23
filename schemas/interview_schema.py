from datetime import datetime
from pydantic import BaseModel, ConfigDict

class QuestionResponse(BaseModel):
    id: str
    question_text: str

    model_config = ConfigDict(
        from_attributes=True
    )

class InterviewResponse(BaseModel):
    id: str
    role_target: str | None
    status: str
    created_at: datetime
    questions: list[QuestionResponse]

    model_config = ConfigDict(
        from_attributes=True
    )

class InterviewListResponse(BaseModel):
    id: str
    role_target: str | None
    status: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )

class InterviewPaginationResponse(BaseModel):
    items: list[InterviewListResponse]
    page: int
    size: int
    total: int
    pages: int

class AnswerDetailResponse(BaseModel):
    id: str
    score: int
    feedback: str
    suggested_improvement: str | None = None

    model_config = ConfigDict(
        from_attributes=True
    )

class QuestionDetailResponse(BaseModel):
    id: str
    question_text: str
    answer: AnswerDetailResponse | None = None

    model_config = ConfigDict(
        from_attributes=True
    )

class InterviewStatisticsResponse(BaseModel):
    total_questions: int
    answered_questions: int
    average_score: float
    completion_percentage: float

class InterviewDetailResponse(BaseModel):
    id: str
    role_target: str | None
    status: str
    created_at: datetime
    statistics: InterviewStatisticsResponse
    questions: list[QuestionDetailResponse]

    model_config = ConfigDict(
        from_attributes=True
    )
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
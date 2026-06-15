from datetime import datetime
from pydantic import BaseModel

class RecentInterviewResponse(BaseModel):
    id: str
    role_target: str
    status: str
    created_at: datetime

    class Config:
        from_attributes=True

class DashboardResponse(BaseModel):
    total_resumes: int
    total_interviews: int
    completed_interviews: int
    average_interview_score: float
    recent_interviews: list[RecentInterviewResponse]
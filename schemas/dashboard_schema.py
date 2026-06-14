from pydantic import BaseModel

class DashboardResponse(BaseModel):
    total_resumes: int
    total_interviews: int
    completed_interviews: int
    average_interview_score: float
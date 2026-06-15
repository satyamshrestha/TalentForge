from pydantic import BaseModel

class InterviewSummaryResponse(BaseModel):
    interview_id: str
    average_score: float
    total_questions: int
    answered_questions: int
    strengths: list[str]
    weaknesses: list[str]
    overall_feedback: str
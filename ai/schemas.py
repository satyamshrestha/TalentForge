from pydantic import BaseModel


class ResumeAnalysisResponse(BaseModel):
    summary: str
    technical_skills: list[str]
    strengths: list[str]
    areas_for_improvement: list[str]


class QuestionGenerationResponse(BaseModel):
    questions: list[str]


class AnswerEvaluationResponse(BaseModel):
    score: int
    feedback: str
    suggested_improvement: str
from pydantic import BaseModel, ConfigDict


class ResumeAnalysisResponse(BaseModel):
    """
    Parser-based resume analysis.
    Generated from extracted resume data.
    """
    resume_score: int
    skills_count: int
    education_count: int
    experience_count: int
    backend_skills: list[str]
    strengths: list[str]
    weaknesses: list[str]


class ResumeAIAnalysisResponse(BaseModel):
    """
    LLM-generated recruiter-style resume analysis.
    """
    summary: str
    technical_skills: list[str]
    strengths: list[str]
    areas_for_improvement: list[str]


class ParsedResumeResponse(BaseModel):
    """
    Structured resume extraction result.
    """
    raw_text: str

    name: str | None = None
    email: str | None = None
    phone: str | None = None

    skills: list[str] = []
    education: list[str] = []
    experience: list[str] = []

    pages: int | None = None

    # Existing parser analysis
    analysis: ResumeAnalysisResponse | None = None

    # AI recruiter analysis
    ai_analysis: ResumeAIAnalysisResponse | None = None


class ResumeResponse(BaseModel):
    id: str
    file_path: str

    parsed_text: ParsedResumeResponse | None

    status: str
    error_message: str | None

    user_id: str

    model_config = ConfigDict(
        from_attributes=True
    )
from ai.provider_factory import get_provider
from ai.prompts import RESUME_ANALYSIS_PROMPT
from ai.schemas import ResumeAnalysisResponse
from ai.utils.parser import parse_ai_response

class ResumeAnalyzer:
    def __init__(self):
        self.provider = get_provider()

    def analyze(self, resume_text: str) -> ResumeAnalysisResponse:
        prompt = RESUME_ANALYSIS_PROMPT.format(resume=resume_text)
        response = self.provider.generate(prompt)

        return parse_ai_response(
            response,
            ResumeAnalysisResponse
        )
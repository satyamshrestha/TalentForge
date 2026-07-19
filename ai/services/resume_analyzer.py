import json

from ai.provider_factory import get_provider
from ai.prompts import RESUME_ANALYSIS_PROMPT
from ai.schemas import ResumeAnalysisResponse
from exceptions.ai_exception import AIResponseFormatException


class ResumeAnalyzer:
    def __init__(self):
        self.provider = get_provider()

    def analyze(self, resume_text: str) -> str:
        prompt = RESUME_ANALYSIS_PROMPT.format(resume=resume_text)
        response = self.provider.generate(prompt)

        try:
            data = json.loads(response)
        except json.JSONDecodeError:
            raise AIResponseFormatException()
        
        return ResumeAnalysisResponse(**data)
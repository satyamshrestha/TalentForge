from ai.provider_factory import get_provider
from ai.prompts import RESUME_ANALYSIS_PROMPT


class ResumeAnalyzer:
    def __init__(self):
        self.provider = get_provider()

    def analyze(self, resume_text: str) -> str:
        prompt = RESUME_ANALYSIS_PROMPT.format(resume=resume_text)
        return self.provider.generate(prompt)
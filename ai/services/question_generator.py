from ai.provider_factory import get_provider
from ai.prompts import QUESTION_GENERATION_PROMPT


class QuestionGenerator:
    def __init__(self):
        self.provider = get_provider()

    def generate(self, resume_text: str) -> str:
        prompt = QUESTION_GENERATION_PROMPT.format(resume=resume_text)
        return self.provider.generate(prompt)
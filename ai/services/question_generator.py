from ai.provider_factory import get_provider
from ai.prompts import QUESTION_GENERATION_PROMPT
from ai.schemas import QuestionGenerationResponse
from ai.utils.parser import parse_ai_response



class QuestionGenerator:
    def __init__(self):
        self.provider = get_provider()

    def generate(self, resume_text: str) -> str:
        prompt = QUESTION_GENERATION_PROMPT.format(resume=resume_text)
        response = self.provider.generate(prompt)

        return parse_ai_response(
            response,
            QuestionGenerationResponse
        )
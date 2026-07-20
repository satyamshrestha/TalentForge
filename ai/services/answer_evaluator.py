from ai.provider_factory import get_provider
from ai.prompts import ANSWER_EVALUATION_PROMPT
from ai.schemas import AnswerEvaluationResponse
from ai.utils.parser import parse_ai_response

class AnswerEvaluator:
    def __init__(self):
        self.provider = get_provider()

    def evaluate(
        self,
        question: str,
        answer: str,
    ) -> str:
        prompt = ANSWER_EVALUATION_PROMPT.format(
            question=question,
            answer=answer,
        )

        response = self.provider.generate(prompt)

        return parse_ai_response(
            response,
            AnswerEvaluationResponse
        )
        
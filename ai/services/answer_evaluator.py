import json

from ai.provider_factory import get_provider
from ai.prompts import ANSWER_EVALUATION_PROMPT
from ai.schemas import AnswerEvaluationResponse
from exceptions.ai_exception import AIResponseFormatException


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

        print("=" * 80)
        print(response)
        print("=" * 80)

        try:
            data = json.loads(response)
        except json.JSONDecodeError:
            raise AIResponseFormatException()

        return AnswerEvaluationResponse(**data)
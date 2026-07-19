import json

from ai.provider_factory import get_provider
from ai.prompts import ANSWER_EVALUATION_PROMPT
from ai.schemas import AnswerEvaluationResponse


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


        data = json.loads(response)

        return AnswerEvaluationResponse(**data)
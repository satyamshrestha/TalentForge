from ai.provider_factory import get_provider
from ai.prompts import ANSWER_EVALUATION_PROMPT


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

        return self.provider.generate(prompt)
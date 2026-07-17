from ai.provider_factory import get_provider


class AnswerEvaluator:
    def __init__(self):
        self.provider = get_provider()

    def evaluate(
        self,
        question: str,
        answer: str,
    ) -> str:
        prompt = f"""
You are an expert technical interviewer.

Question:
{question}

Candidate Answer:
{answer}

Provide:

## Score (1-10)
## Feedback
## Suggested Improvement

Keep the response concise.
"""

        return self.provider.generate(prompt)
from ai.provider_factory import get_provider


class QuestionGenerator:
    def __init__(self):
        self.provider = get_provider()

    def generate(self, resume_text: str) -> str:
        prompt = f"""
You are a senior technical interviewer.

Based on the following resume, generate exactly 5 interview questions.

Requirements:
- Questions should match the candidate's skills.
- Include a mix of theory and practical questions.
- Return only the numbered questions.

Resume:
{resume_text}
"""

        return self.provider.generate(prompt)
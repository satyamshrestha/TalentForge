from ai.provider_factory import get_provider


class ResumeAnalyzer:
    def __init__(self):
        self.provider = get_provider()

    def analyze(self, resume_text: str) -> str:
        prompt = f"""
You are an expert technical recruiter.

Analyze the following resume and provide:

1. A brief summary of the candidate.
2. Key technical skills.
3. Strengths.
4. Areas for improvement.

Resume:
{resume_text}
"""

        return self.provider.generate(prompt)
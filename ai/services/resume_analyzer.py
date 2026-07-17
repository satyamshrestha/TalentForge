from ai.provider_factory import get_provider


class ResumeAnalyzer:
    def __init__(self):
        self.provider = get_provider()

    def analyze(self, resume_text: str) -> str:
        prompt = f"""
You are an expert technical recruiter.

Analyze the resume below.

Return ONLY these sections:

## Summary
## Technical Skills
## Strengths
## Areas for Improvement

Keep the response concise (maximum 200 words).

Resume:
{resume_text}
"""

        return self.provider.generate(prompt)
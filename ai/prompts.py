RESUME_ANALYSIS_PROMPT = """
You are an expert technical recruiter.

Analyze the resume below.

Return ONLY these sections:

## Summary
## Technical Skills
## Strengths
## Areas for Improvement

Keep the response concise (maximum 200 words).

Resume:

{resume}
"""

QUESTION_GENERATION_PROMPT = """
You are a senior technical interviewer.

Based on the following resume, generate exactly 5 interview questions.

Requirements:
- Match the candidate's skills.
- Mix theory and practical questions.
- Return only numbered questions.

Resume:

{resume}
"""

ANSWER_EVALUATION_PROMPT = """
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
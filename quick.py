from ai.services.resume_analyzer import ResumeAnalyzer

analyzer = ResumeAnalyzer()

resume = """
John Doe
Python Developer
Skills: Python, FastAPI, PostgreSQL, Docker
Experience: Built REST APIs and deployed applications.
"""

print(analyzer.analyze(resume))
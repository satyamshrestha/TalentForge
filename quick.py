from ai.services.resume_analyzer import ResumeAnalyzer
from ai.services.question_generator import QuestionGenerator


# analyzer = ResumeAnalyzer()

# resume = """
# John Doe
# Python Developer
# Skills: Python, FastAPI, PostgreSQL, Docker
# Experience: Built REST APIs and deployed applications.
# """

# print(analyzer.analyze(resume))

generator = QuestionGenerator()

print(
    generator.generate(
        "Python, FastAPI, PostgreSQL, Docker"
    )
)
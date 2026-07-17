from ai.services.resume_analyzer import ResumeAnalyzer
from ai.services.question_generator import QuestionGenerator
from ai.services.answer_evaluator import AnswerEvaluator


# analyzer = ResumeAnalyzer()

# resume = """
# John Doe
# Python Developer
# Skills: Python, FastAPI, PostgreSQL, Docker
# Experience: Built REST APIs and deployed applications.
# """

# print(analyzer.analyze(resume))

# generator = QuestionGenerator()

# print(
#     generator.generate(
#         "Python, FastAPI, PostgreSQL, Docker"
#     )
# )

evaluator = AnswerEvaluator()

print(
    evaluator.evaluate(
        "What is FastAPI?",
        "FastAPI is a Python web framework."
    )
)
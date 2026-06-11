QUESTION_BANK = {
    "Python": [
        "Explain Python decorators.",
        "What are generators in Python?"
    ],
    "FastAPI": [
        "What is Dependency Injection in FastAPI?",
        "How does FastAPI handle request validation?"
    ],
    "Redis": [
        "Why use Redis for caching?",
        "What is cache invalidation?"
    ],
    "Docker": [
        "Difference between image and container?",
        "What is a Docker volume?"
    ]
}

class QuestionGenerator:

    def generate(
        self,
        skills: list[str]
    ):
        questions = []

        for skill in skills:
            skill_questions = QUESTION_BANK.get(skill, [])
            questions.extend(skill_questions)

        questions = list(dict.fromkeys(questions))
        return questions
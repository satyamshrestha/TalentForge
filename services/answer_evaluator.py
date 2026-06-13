class AnswerEvaluator:

    QUESTION_KEYWORDS = {
        "Explain Python decorators.": {
            "decorator",
            "decorators",
            "function",
            "wrapper"
        },

        "What are generators in Python?": {
            "generator",
            "generators",
            "yield",
            "iterator"
        },

        "What is Dependency Injection in FastAPI?": {
            "dependency",
            "injection",
            "depends",
            "fastapi"
        },

        "How does FastAPI handle request validation?": {
            "validation",
            "pydantic",
            "request",
            "schema",
            "fastapi"
        },

        "Why use Redis for caching?": {
            "redis",
            "cache",
            "caching",
            "memory",
            "performance"
        },

        "What is cache invalidation?": {
            "cache",
            "invalidation",
            "stale",
            "update",
            "refresh"
        },

        "Difference between image and container?": {
            "image",
            "container",
            "docker",
            "template",
            "running"
        },

        "What is a Docker volume?": {
            "volume",
            "storage",
            "persistent",
            "data",
            "docker"
        }
    }

    def evaluate(
        self,
        question_text: str,
        answer_text: str
    ):
        score = 0
        feedback = []

        # Length Score (0-5)
        word_count = len(answer_text.split())

        if word_count >= 10:
            score += 2
        else:
            feedback.append("Answer is too short.")
        if word_count >= 25:
            score += 2
        if word_count >= 50:
            score += 1

        # Keyword Score (0-5)
        expected_keywords = self.QUESTION_KEYWORDS.get(question_text, set())
        answer_words = {
            word.lower().strip(".,!?():;")
            for word in answer_text.split()
        }
        matched_keywords = (
            expected_keywords &
            answer_words
        )

        score += min(
            len(matched_keywords),
            5
        )
        if matched_keywords:
            feedback.append(f"Relevant concepts detected: {', '.join(sorted(matched_keywords))}.")
        else:
            feedback.append("No important or relevant concepts detected.")

        return {
            "score": min(score, 10),
            "feedback": " ".join(feedback)
        }
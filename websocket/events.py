from enum import Enum


class WebSocketEvent(str, Enum):
    INTERVIEW_STARTED = "interview.started"
    QUESTION_AVAILABLE = "question.available"
    ANSWER_SUBMITTED = "answer.submitted"
    ANSWER_EVALUATED = "answer.evaluated"
    INTERVIEW_COMPLETED = "interview.completed"
    ERROR = "error"
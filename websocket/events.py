from enum import Enum


class WebSocketEvent(str, Enum):
    INTERVIEW_STARTED = "interview.started"
    ANSWER_SUBMITTED = "answer.submitted"
    ANSWER_EVALUATED = "answer.evaluated"
    ERROR = "error"
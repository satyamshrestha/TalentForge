from exceptions.app_exception import AppException

class QuestionAlreadyAnsweredException(AppException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="Question already answered."
        )
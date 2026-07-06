from exceptions.app_exception import AppException

class QuestionNotFoundException(AppException):
    def __init__(self):
        super().__init__(
            status_code=404,
            detail="Question doesn't exist!"
        )
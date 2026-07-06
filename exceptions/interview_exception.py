from exceptions.app_exception import AppException

class InterviewNotFoundException(AppException):
    def __init__(self):
        super().__init__(
            status_code=404,
            detail="Interview not found!"
        )

class InterviewAccessDeniedException(AppException):
    def __init__(self):
        super().__init__(
            status_code=403,
            detail="Access denied!"
        )

class ResumeSkillsNotFoundException(AppException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="No backend skills found in resume."
        )
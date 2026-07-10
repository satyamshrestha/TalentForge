from exceptions.app_exception import AppException


class InvalidResumeFileException(AppException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="Only PDF files are allowed."
        )

class ResumeNotFoundException(AppException):
    def __init__(self):
        super().__init__(
            status_code=404,
            detail="Resume does not exist!"
        )

class ResumeAccessDeniedException(AppException):
    def __init__(self):
        super().__init__(
            status_code=403,
            detail="Resume does not belong to the current user!"
        )

class ResumeTooLargeException(AppException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="Resume exceeds maximum size of 5 MB."
        )

class InvalidResumeContentException(AppException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="Uploaded file is not a valid PDF."
        )
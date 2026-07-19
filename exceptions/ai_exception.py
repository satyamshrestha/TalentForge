from exceptions.app_exception import AppException


class AIProviderException(AppException):
    def __init__(self):
        super().__init__(
            status_code=500,
            detail="AI provider is unavailable."
        )


class AIResponseFormatException(AppException):
    def __init__(self):
        super().__init__(
            status_code=500,
            detail="AI returned an invalid response format."
        )
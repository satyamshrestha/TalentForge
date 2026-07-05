class AppException(Exception):
    def __init__(
        self,
        status_code: int,
        detail: str,
    ):
        self.status_code = status_code
        self.detail = detail

class UserAlreadyExistsException(AppException):
    def __init__(self):
        super().__init__(
            status_code=409,
            detail="User already exists!"
        )

class UserNotFoundException(AppException):
    def __init__(self):
        super().__init__(
            status_code=404,
            detail="User doesn't exist!"
        )

class InvalidCredentialsException(AppException):
    def __init__(self):
        super().__init__(
            status_code=401,
            detail="Invalid credentials!"
        )

class GoogleAccountException(AppException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="Please sign in with Google."
        )

class InvalidRefreshTokenException(AppException):
    def __init__(self):
        super().__init__(
            status_code=401,
            detail="Invalid refresh token!"
        )

class GoogleAlreadyLinkedException(AppException):
    def __init__(self):
        super().__init__(
            status_code=409,
            detail="This Google account is already linked to another user."
        )
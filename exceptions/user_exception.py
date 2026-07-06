from exceptions.app_exception import AppException


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

class LocalAccountExistsException(AppException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail=(
                "An account with this email already exists. "
                "Please sign in using your email and password instead of Google."
            )
        )

class PasswordChangeNotAllowedException(AppException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="Google accounts cannot change passwords."
        )

class CurrentPasswordIncorrectException(AppException):
    def __init__(self):
        super().__init__(
            status_code=401,
            detail="Current password is incorrect."
        )

class PasswordReuseException(AppException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="New password must be different from the current password."
        )
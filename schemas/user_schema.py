from pydantic import BaseModel, EmailStr, ConfigDict

class UserSignup(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    email: EmailStr

    model_config = ConfigDict(
        from_attributes=True
    )

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class ProfileResponse(BaseModel):
    id: str
    full_name: str | None = None
    email: str
    role: str
    provider: str
    google_connected: bool

    model_config = ConfigDict(
        from_attributes=True
    )

class ProfileUpdate(BaseModel):
    full_name: str | None = None

class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str
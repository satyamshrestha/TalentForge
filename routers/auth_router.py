from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from schemas.user_schema import UserSignup, UserResponse, TokenResponse, RefreshTokenRequest
from auth.deps import get_current_user
from db.deps import get_db
from models.user import User
from services.deps import get_user_service
from services.user_service import UserService

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup", response_model=UserResponse, status_code=201)
def signup(
    data: UserSignup,
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service)
):
    return service.signup(
        db,
        email=data.email,
        password=data.password
    )

@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service)
):
    return service.login(
        db,
        email=form_data.username,
        password=form_data.password
    )

@router.get("/me")
def get_me(
    current_user: User = Depends(get_current_user)
):
    return {
        "ID": current_user.id,
        "Email": current_user.email
    }

@router.post("/refresh")
def refresh_token(
    data: RefreshTokenRequest,
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service)
):
    return service.refresh_access_token(db, data.refresh_token)
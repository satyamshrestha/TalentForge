from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from auth.google_oauth import oauth
from auth.scope_deps import require_scope
from schemas.user_schema import UserSignup, UserResponse, TokenResponse, RefreshTokenRequest
from auth.deps import get_current_user
from db.deps import get_db
from models.user import User
from services.deps import get_user_service
from services.user_service import UserService
from utils.config import settings

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.get("/google/login", include_in_schema=False)
async def google_login(request: Request):
    redirect_uri = settings.GOOGLE_REDIRECT_URI
    return await oauth.google.authorize_redirect(
        request,
        redirect_uri
    )

@router.get("/google/callback", include_in_schema=False)
async def google_callback(
    request: Request,
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service)
):
    token = await oauth.google.authorize_access_token(request)

    user_info = token["userinfo"]

    return service.google_login(db, user_info)

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
        "Email": current_user.email,
        "Role": current_user.role
    }

@router.post("/refresh")
def refresh_token(
    data: RefreshTokenRequest,
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service)
):
    return service.refresh_access_token(db, data.refresh_token)

@router.get("/scope-test")
def scope_test(
    current_user=Depends(require_scope("admin"))
):
    return {
        "message": "Admin scope works!"
    }
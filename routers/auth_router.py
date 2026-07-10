from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from auth.google_oauth import oauth
from auth.oauth_state import generate_state
from auth.scope_deps import require_scope
from schemas.user_schema import UserSignup, UserResponse, TokenResponse, RefreshTokenRequest
from auth.deps import get_current_user
from db.deps import get_db
from middleware.rate_limit import limiter
from models.user import User
from services.deps import get_user_service
from services.user_service import UserService
from utils.config import settings

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.get("/google/login", include_in_schema=False)
@limiter.limit("10/minute")
async def google_login(request: Request):
    state = generate_state()
    request.session["oauth_state"] = state
    
    return await oauth.google.authorize_redirect(
        request,
        settings.GOOGLE_REDIRECT_URI,
        state=state
    )

@router.get("/google/callback", include_in_schema=False)
async def google_callback(
    request: Request,
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service)
):
    returned_state = request.query_params.get("state")
    expected_state = request.session.get("oauth_state")

    if not expected_state or returned_state != expected_state:
        raise HTTPException(
            status_code=400,
            detail="Invalid OAuth state."
        )

    request.session.pop("oauth_state", None)
    token = await oauth.google.authorize_access_token(request)
    user_info = token["userinfo"]

    return service.google_login(db, user_info)

@router.get("/google/connect", include_in_schema=False)
@limiter.limit("10/minute")
async def connect_google(
    request: Request,
    current_user: User = Depends(get_current_user),
):
    state = generate_state()
    request.session["oauth_state"] = state
    
    return await oauth.google.authorize_redirect(
        request,
        settings.GOOGLE_REDIRECT_URI,
        state=state
    )

@router.get("/google/connect/callback", include_in_schema=False)
async def google_connect_callback(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    service: UserService = Depends(get_user_service)
):
    returned_state = request.query_params.get("state")
    saved_state = request.session.get("oauth_state")

    if not saved_state or returned_state != saved_state:
        raise HTTPException(
            status_code=400,
            detail="Invalid OAuth state."
        )

    request.session.pop("oauth_state", None)
    token = await oauth.google.authorize_access_token(request)
    user_info = token["userinfo"]
    
    return service.connect_google(
        db=db,
        current_user=current_user,
        user_info=user_info,
    )

@router.post("/signup", response_model=UserResponse, status_code=201)
@limiter.limit("5/minute")
def signup(
    request: Request,
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
@limiter.limit("5/minute")
def login(
    request: Request,
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
@limiter.limit("20/minute")
def refresh_token(
    request: Request,
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
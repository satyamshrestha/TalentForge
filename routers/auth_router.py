from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from schemas.user_schema import UserSignup, UserResponse
from db.deps import get_db
from services.deps import get_user_service
from services.user_service import UserService

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("", response_model=UserResponse)
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
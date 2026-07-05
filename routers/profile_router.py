from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from auth.deps import get_current_user
from db.deps import get_db
from models.user import User
from schemas.user_schema import ProfileResponse, ProfileUpdate, PasswordChangeRequest
from services.deps import get_user_service
from services.user_service import UserService

router = APIRouter(prefix="/profile", tags=["Profile"])

@router.get("", response_model=ProfileResponse)
def get_profile(
    current_user: User = Depends(get_current_user),
    service: UserService = Depends(get_user_service)
):
    return service.get_profile(current_user)

@router.patch("/update", response_model=ProfileResponse)
def update_profile(
    data: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service)
):
    return service.update_profile(db, data, current_user)

@router.patch("/change-password")
def update_password(
    data: PasswordChangeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service)
):
    return service.change_password(db, current_user, data)
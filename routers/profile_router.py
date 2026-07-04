from fastapi import APIRouter, Depends

from auth.deps import get_current_user
from models.user import User
from schemas.user_schema import ProfileResponse
from services.deps import get_user_service
from services.user_service import UserService

router = APIRouter(prefix="/profile", tags=["Profile"])

@router.get(
    "",
    response_model=ProfileResponse
)
def get_profile(
    current_user: User = Depends(get_current_user),
    service: UserService = Depends(get_user_service)
):
    return service.get_profile(current_user)
from fastapi import APIRouter, Depends

from auth.role_deps import require_roles

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

@router.get("/ping")
def admin_ping(
    current_user=Depends(require_roles("admin"))
):
    return {
        "message": f"Hello Admin, {current_user.email}!"
    }
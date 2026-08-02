from fastapi import APIRouter, Depends

from auth.role_deps import require_roles

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    responses={
        401: {
            "description": "Authentication required"
        },
        403: {
            "description": "Admin privileges required"
        },
    },
)


@router.get(
    "/ping",
    summary="Admin health check",
    description="Verifies that the authenticated user has admin privileges.",
)
def admin_ping(
    current_user=Depends(require_roles("admin"))
):
    return {
        "message": f"Hello Admin, {current_user.email}!"
    }
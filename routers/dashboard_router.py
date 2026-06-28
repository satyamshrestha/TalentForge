from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from auth.scope_deps import require_scope
from db.deps import get_db
from models.user import User
from schemas.dashboard_schema import DashboardResponse
from services.deps import get_dashboard_service
from services.dashboard_service import DashboardService

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("", response_model=DashboardResponse)
def get_dashboard(
    current_user: User = Depends(require_scope("dashboard:read")),
    db: Session = Depends(get_db),
    service: DashboardService = Depends(get_dashboard_service)
):
    return service.get_dashboard(db, current_user)
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from db.deps import get_db
from db.redis import redis_client


router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get(
    "/live",
    summary="Liveness Probe",
    description=(
        "Checks whether the application process "
        "is running."
    ),
)
def liveness():
    return {
        "status": "alive"
    }


@router.get(
    "/ready",
    summary="Readiness Probe",
    description=(
        "Checks whether the application can "
        "handle requests by verifying database "
        "and Redis connectivity."
    ),
    responses={
        503: {
            "description": "Service dependencies unavailable"
        },
    },
)
def readiness(
    db: Session = Depends(get_db),
):
    try:
        db.execute(text("SELECT 1"))
        redis_client.ping()

        return {
            "status": "ready",
            "database": "connected",
            "redis": "connected",
        }

    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Service unavailable",
        )
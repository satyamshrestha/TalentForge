from fastapi import APIRouter
from sqlalchemy import text

from db.database import engine
from db.redis import redis_client


router = APIRouter(
    prefix="/health",
    tags=["Health"]
)


@router.get("")
def health_check():
    return {
        "status": "ok"
    }


@router.get("/ready")
def readiness_check():

    checks = {
        "database": "unknown",
        "redis": "unknown"
    }

    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        checks["database"] = "ok"

    except Exception:
        checks["database"] = "failed"


    try:
        redis_client.ping()

        checks["redis"] = "ok"

    except Exception:
        checks["redis"] = "failed"


    ready = all(
        value == "ok"
        for value in checks.values()
    )

    return {
        "status": "ready" if ready else "not_ready",
        **checks
    }
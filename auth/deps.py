from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from auth.oauth2 import oauth2_scheme
from auth.jwt_handler import verify_access_token
from db.deps import get_db
from repositories.user_repository import UserRepository


def get_token_payload(
    token: str = Depends(oauth2_scheme)
):
    payload = verify_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token!"
        )

    return payload

def get_current_user(
    payload=Depends(get_token_payload),
    db: Session = Depends(get_db)
):
    user_id = payload.get("sub")

    repository = UserRepository()
    user = repository.get_by_id(db, user_id)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found!"
        )

    return user
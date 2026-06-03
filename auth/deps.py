from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from auth.jwt_handler import verify_access_token
from auth.oauth2 import oauth2_scheme
from db.deps import get_db
from repositories.user_repository import UserRepository

def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):
    payload = verify_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid Token!")
    
    user_id = payload.get("sub")
    repository = UserRepository()

    user = repository.get_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found!"
        )

    return user
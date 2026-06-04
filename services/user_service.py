import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException

from auth.hashing import hash_password, verify_password
from auth.jwt_handler import create_access_token, create_refresh_token, verify_refresh_token
from models.user import User
from repositories.user_repository import UserRepository

class UserService:
    def __init__(
        self,
        repository: UserRepository
    ):
        self.repository = repository

    def signup(
        self,
        db: Session,
        email: str,
        password: str
    ):
        existing_user = self.repository.get_by_email(db, email)
        if existing_user:
            raise HTTPException(status_code=409, detail="User already exists!")

        user = User(
            id=str(uuid.uuid4()),
            email=email,
            password=hash_password(password)
        )
        return self.repository.create_user(db, user)
    
    def login(
        self,
        db: Session,
        email: str,
        password: str
    ):
        user = self.repository.get_by_email(db, email)
        if not user:
            raise HTTPException(status_code=404, detail="User doesn't exist!")
        if not verify_password(password, user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials!")
        
        access_token = create_access_token({"sub": user.id})
        refresh_token = create_refresh_token({"sub": user.id})

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
    
    def refresh_access_token(
        self,
        db: Session,
        refresh_token: str
    ):
        payload = verify_refresh_token(refresh_token)
        if payload is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid refresh token!"
            )
        user_id = payload.get("sub")
        user = self.repository.get_by_id(db, user_id)

        if not user:
            raise HTTPException(
                status_code=401,
                detail="User not found!"
            )
        access_token = create_access_token({"sub": user_id})

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
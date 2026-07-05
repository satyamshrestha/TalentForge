import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException

from auth.hashing import hash_password, verify_password
from auth.jwt_handler import create_access_token, create_refresh_token, verify_refresh_token
from models.user import User
from repositories.user_repository import UserRepository
from schemas.user_schema import ProfileUpdate, PasswordChangeRequest
from auth.scopes import ROLE_SCOPES

class UserService:
    def __init__(
        self,
        user_repository: UserRepository
    ):
        self.user_repository = user_repository

    def google_login(
        self,
        db: Session,
        user_info: dict
    ):
        google_id = user_info["sub"]
        email = user_info["email"]

        google_user = self.user_repository.get_by_google_id(db, google_id)
        if google_user:
            user = google_user
        else:
            user = self.user_repository.get_by_email(db, email)
            if user and user.provider == "local":
                raise HTTPException(status_code=400, detail="An account with this email already exists. Please sign in using your email and password instead of Google.") 
            if user and user.provider == "google":
                if user.google_id is None:
                    user = self.user_repository.update_google_id(db, user, google_id)
            if not user:
                user = User(
                    id=str(uuid.uuid4()),
                    full_name=user_info["name"],
                    email=email,
                    password=None,
                    provider="google",
                    google_id=google_id,
                    role="student",
                )
                user = self.user_repository.create_user(db, user)

        return self._generate_tokens(user)
    
    def connect_google(
        self,
        db: Session,
        current_user: User,
        user_info: dict
    ):
        google_id = user_info["sub"]

        existing_google_user = self.user_repository.get_by_google_id(db, google_id)

        if existing_google_user:
            if existing_google_user.id != current_user.id:
                raise HTTPException(
                    status_code=409,
                    detail="This Google account is already linked to another user."
                )

            return {
                "message": "Google account already connected."
            }

        self.user_repository.update_google_id(
            db,
            current_user,
            google_id
        )

        return {
            "message": "Google account connected successfully."
        }

    def signup(
        self,
        db: Session,
        email: str,
        password: str
    ):
        existing_user = self.user_repository.get_by_email(db, email)
        if existing_user:
            raise HTTPException(status_code=409, detail="User already exists!")

        user = User(
            id=str(uuid.uuid4()),
            full_name=None,
            email=email,
            password=hash_password(password),
            provider="local",
            role="student"
        )
        return self.user_repository.create_user(db, user)
    
    def login(
        self,
        db: Session,
        email: str,
        password: str
    ):
        user = self.user_repository.get_by_email(db, email)
        if not user:
            raise HTTPException(status_code=404, detail="User doesn't exist!")
        if user.provider == "google":
            raise HTTPException(status_code=400, detail="Please sign in with Google.")
        if not verify_password(password, user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials!")
        
        return self._generate_tokens(user)
    
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
        user = self.user_repository.get_by_id(db, user_id)

        if not user:
            raise HTTPException(
                status_code=401,
                detail="User not found!"
            )
        access_token = create_access_token(
            {
                "sub": str(user.id),
                "role": user.role,
                "scopes": ROLE_SCOPES.get(user.role, [])
            }
        )

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    
    def get_profile(
        self,
        current_user: User,
    ):
        return {
            "id": current_user.id,
            "full_name": current_user.full_name,
            "email": current_user.email,
            "role": current_user.role,
            "provider": current_user.provider,
            "google_connected": current_user.google_id is not None,
        }
    
    def update_profile(
        self,
        db: Session,
        data: ProfileUpdate,
        current_user: User
    ):
        current_user.full_name = data.full_name
        self.user_repository.commit_and_refresh(db, current_user)
        return self.get_profile(current_user)
    
    def change_password(
        self,
        db: Session,
        current_user: User,
        data: PasswordChangeRequest,
    ):
        if current_user.provider == "google":
            raise HTTPException(status_code=400, detail="Google accounts cannot change passwords.")
        
        if not verify_password(data.current_password, current_user.password):
            raise HTTPException(status_code=401, detail="Current password is incorrect.")
        
        if verify_password(data.new_password, current_user.password):
            raise HTTPException(status_code=400, detail="New password must be different from the current password.")
        
        current_user.password = hash_password(data.new_password)
        self.user_repository.commit_and_refresh(db, current_user)
        return {"message": "Password updated successfully."}

    def _generate_tokens(
        self,
        user: User
    ):
        access_token = create_access_token(
            {
                "sub": str(user.id),
                "role": user.role,
                "scopes": ROLE_SCOPES.get(user.role, [])
            }
        )

        refresh_token = create_refresh_token(
            {
                "sub": str(user.id),
                "role": user.role,
                "scopes": ROLE_SCOPES.get(user.role, [])
            }
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }